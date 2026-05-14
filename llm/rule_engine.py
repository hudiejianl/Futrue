from __future__ import annotations


LEVEL_NAME = {
    0: "normal",
    1: "slight",
    2: "moderate",
    3: "severe",
}


def evaluate_rules(summary: dict) -> list[dict]:
    hits = []
    wear_level = int(summary.get("wear_level", -1))
    wear_value = float(summary.get("predicted_wear", 0.0))
    gt_wear = summary.get("ground_truth_wear")

    if wear_level in LEVEL_NAME:
        hits.append(
            {
                "rule_id": f"wear_{LEVEL_NAME[wear_level]}",
                "reason": f"磨损等级为 {LEVEL_NAME[wear_level]}",
            }
        )

    if wear_value > 0.30:
        hits.append(
            {
                "rule_id": "high_wear_value",
                "reason": f"预测磨损值 {wear_value:.4f} > 0.30",
            }
        )
    elif wear_value > 0.20:
        hits.append(
            {
                "rule_id": "mid_wear_value",
                "reason": f"预测磨损值 {wear_value:.4f} > 0.20",
            }
        )

    if summary.get("primary_model") == "force_only":
        hits.append(
            {
                "rule_id": "force_regression_reference",
                "reason": "当前主预测模型为 Force-only",
            }
        )

    if summary.get("use_image_context", False):
        hits.append(
            {
                "rule_id": "image_auxiliary_reference",
                "reason": "当前启用了图像辅助解释",
            }
        )

    if gt_wear is not None:
        diff = abs(float(gt_wear) - wear_value)
        hits.append(
            {
                "rule_id": "prediction_trace",
                "reason": f"预测值与标签差异为 {diff:.4f}",
            }
        )

    return hits
