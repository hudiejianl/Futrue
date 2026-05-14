from __future__ import annotations


LEVEL_MAP = {
    0: "正常",
    1: "轻度磨损",
    2: "中度磨损",
    3: "重度磨损",
}


def generate_report(summary: dict, knowledge_items: list[dict]) -> str:
    wear_level = int(summary.get("wear_level", -1))
    wear_value = float(summary.get("predicted_wear", 0.0))
    cycle_id = summary.get("cycle_id", "unknown")
    level_text = LEVEL_MAP.get(wear_level, "未知")

    evidence_lines = []
    advice_lines = []
    for item in knowledge_items:
        title = item.get("title", "")
        reason = item.get("reason", "")
        advice = item.get("advice", "")
        if title:
            evidence_lines.append(f"- {title}：{reason}")
        if advice:
            advice_lines.append(f"- {advice}")

    if not evidence_lines:
        evidence_lines.append("- 暂无命中的规则证据。")
    if not advice_lines:
        advice_lines.append("- 暂无明确建议，请结合人工经验进一步判断。")

    replace_flag = "是" if wear_level >= 3 or wear_value > 0.30 else "否"
    risk_level = "高" if wear_level >= 3 else "中" if wear_level == 2 else "低"

    report = [
        f"诊断对象：{cycle_id}",
        f"诊断结论：当前刀具磨损等级为{level_text}，预测磨损值为 {wear_value:.4f}。",
        f"风险等级：{risk_level}",
        "主要依据：",
        *evidence_lines,
        f"是否建议换刀：{replace_flag}",
        "建议操作：",
        *advice_lines,
    ]
    return "\n".join(report)
