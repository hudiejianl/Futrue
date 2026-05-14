from __future__ import annotations

import json
from pathlib import Path


class KnowledgeRetriever:
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.items = json.loads(self.kb_path.read_text(encoding="utf-8"))
        self.item_map = {item["id"]: item for item in self.items}

    def retrieve(self, rule_hits: list[dict]) -> list[dict]:
        results = []
        for hit in rule_hits:
            item = self.item_map.get(hit["rule_id"])
            if item is None:
                continue
            merged = dict(item)
            merged["reason"] = hit.get("reason", "")
            results.append(merged)
        return results
