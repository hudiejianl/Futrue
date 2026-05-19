from __future__ import annotations

import json
from pathlib import Path


class KnowledgeRetriever:
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.items = json.loads(self.kb_path.read_text(encoding="utf-8"))
        self.item_map = {item["id"]: item for item in self.items}

    def _match_conditions(self, summary: dict, item: dict) -> bool:
        conditions = item.get("applicable_conditions", {})

        wear_level = conditions.get("wear_level")
        if wear_level is not None and summary.get("wear_level") not in wear_level:
            return False

        wear_value_min = conditions.get("wear_value_min")
        if wear_value_min is not None and float(summary.get("predicted_wear", 0.0)) < float(wear_value_min):
            return False

        wear_value_max = conditions.get("wear_value_max")
        if wear_value_max is not None and float(summary.get("predicted_wear", 0.0)) > float(wear_value_max):
            return False

        primary_model = conditions.get("primary_model")
        if primary_model is not None and summary.get("primary_model") not in primary_model:
            return False

        use_image_context = conditions.get("use_image_context")
        if use_image_context is not None and bool(summary.get("use_image_context", False)) != bool(use_image_context):
            return False

        prediction_error = summary.get("prediction_error")
        error_min = conditions.get("prediction_error_min")
        if error_min is not None:
            if prediction_error is None or float(prediction_error) < float(error_min):
                return False

        error_max = conditions.get("prediction_error_max")
        if error_max is not None:
            if prediction_error is None or float(prediction_error) > float(error_max):
                return False

        return True

    def _score_item(self, summary: dict, item: dict, rule_hits: list[dict]) -> int:
        score = 0
        hit_ids = {hit["rule_id"] for hit in rule_hits}

        if item["id"] in hit_ids:
            score += 5

        for tag in item.get("case_tag", []):
            if tag in str(summary).lower():
                score += 1

        if self._match_conditions(summary, item):
            score += 2

        return score

    def retrieve(self, rule_hits: list[dict], summary: dict | None = None, top_k: int = 6) -> list[dict]:
        summary = summary or {}
        results = []

        reason_map = {hit["rule_id"]: hit.get("reason", "") for hit in rule_hits}
        for item in self.items:
            if not self._match_conditions(summary, item) and item["id"] not in reason_map:
                continue

            merged = dict(item)
            merged["reason"] = reason_map.get(item["id"], "")
            merged["score"] = self._score_item(summary, item, rule_hits)
            results.append(merged)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
