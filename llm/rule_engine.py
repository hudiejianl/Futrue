from __future__ import annotations


def evaluate_rules(summary: dict) -> list[dict]:
    hits = []
    wear_level = int(summary.get("wear_level", -1))
    wear_value = float(summary.get("predicted_wear", 0.0))

    if wear_level == 0:
        hits.append({"rule_id": "wear_normal", "reason": "磨损等级为 normal"})
    elif wear_level == 1:
        hits.append({"rule_id": "wear_slight", "reason": "磨损等级为 slight"})
    elif wear_level == 2:
        hits.append({"rule_id": "wear_moderate", "reason": "磨损等级为 moderate"})
    elif wear_level == 3:
        hits.append({"rule_id": "wear_severe", "reason": "磨损等级为 severe"})

    if wear_value > 0.30:
        hits.append({"rule_id": "high_wear_value", "reason": f"磨损值 {wear_value:.4f} > 0.30"})
    elif wear_value > 0.20:
        hits.append({"rule_id": "mid_wear_value", "reason": f"磨损值 {wear_value:.4f} > 0.20"})

    if summary.get("primary_model") == "force_only":
        hits.append({"rule_id": "force_regression_reference", "reason": "当前主预测模型为 Force-only"})

    if summary.get("use_image_context", False):
        hits.append({"rule_id": "image_auxiliary_reference", "reason": "当前启用了图像辅助解释"})

    return hits
