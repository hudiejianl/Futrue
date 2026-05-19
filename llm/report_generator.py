from __future__ import annotations

import json
import os
from pathlib import Path


LEVEL_MAP = {
    0: "正常",
    1: "轻度磨损",
    2: "中度磨损",
    3: "重度磨损",
}


def build_structured_result(summary: dict, knowledge_items: list[dict]) -> dict:
    wear_level = int(summary.get("wear_level", -1))
    wear_value = float(summary.get("predicted_wear", 0.0))
    cycle_id = summary.get("cycle_id", "unknown")
    level_text = LEVEL_MAP.get(wear_level, "未知")

    evidence = []
    actions = []
    for item in knowledge_items:
        reason = item.get("reason", "") or item.get("title", "")
        evidence.append(
            {
                "title": item.get("title", ""),
                "reason": reason,
                "risk_level": item.get("risk_level", "info"),
            }
        )
        action = item.get("recommended_action", "")
        if action:
            actions.append(action)

    if not evidence:
        evidence.append(
            {
                "title": "无命中证据",
                "reason": "当前没有匹配到规则证据。",
                "risk_level": "info",
            }
        )

    if not actions:
        actions.append("暂无明确建议，请结合人工经验进一步判断。")

    replace_flag = wear_level >= 3 or wear_value > 0.30
    risk_level = "高" if wear_level >= 3 else "中" if wear_level == 2 else "低"

    return {
        "cycle_id": cycle_id,
        "diagnosis": f"当前刀具磨损等级为{level_text}，预测磨损值为 {wear_value:.4f}。",
        "risk_level": risk_level,
        "replace_tool": replace_flag,
        "evidence": evidence,
        "actions": actions,
    }


def render_structured_result(result: dict) -> str:
    evidence_lines = [f"- {item['title']}：{item['reason']}" for item in result["evidence"]]
    action_lines = [f"- {item}" for item in result["actions"]]
    replace_text = "是" if result["replace_tool"] else "否"

    report = [
        f"诊断对象：{result['cycle_id']}",
        f"诊断结论：{result['diagnosis']}",
        f"风险等级：{result['risk_level']}",
        "主要依据：",
        *evidence_lines,
        f"是否建议换刀：{replace_text}",
        "建议操作：",
        *action_lines,
    ]
    return "\n".join(report)


def generate_openai_report(summary: dict, knowledge_items: list[dict], prompt_template_path: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    from openai import OpenAI

    template = Path(prompt_template_path).read_text(encoding="utf-8")
    client = OpenAI(api_key=api_key)
    content = (
        template
        + "\n\n结构化预测摘要：\n"
        + json.dumps(summary, ensure_ascii=False, indent=2)
        + "\n\n知识库检索结果：\n"
        + json.dumps(knowledge_items, ensure_ascii=False, indent=2)
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=[{"role": "user", "content": content}],
    )
    return response.choices[0].message.content or ""


def generate_deepseek_report(summary: dict, knowledge_items: list[dict], prompt_template_path: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not set")

    from openai import OpenAI

    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

    template = Path(prompt_template_path).read_text(encoding="utf-8")
    client = OpenAI(api_key=api_key, base_url=base_url)
    content = (
        template
        + "\n\n结构化预测摘要：\n"
        + json.dumps(summary, ensure_ascii=False, indent=2)
        + "\n\n知识库检索结果：\n"
        + json.dumps(knowledge_items, ensure_ascii=False, indent=2)
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": content}],
    )
    return response.choices[0].message.content or ""


def generate_report(summary: dict, knowledge_items: list[dict], mode: str = "template", prompt_template_path: str | None = None) -> str:
    if mode == "openai":
        if not prompt_template_path:
            raise ValueError("prompt_template_path is required when mode='openai'")
        return generate_openai_report(summary, knowledge_items, prompt_template_path)
    if mode == "deepseek":
        if not prompt_template_path:
            raise ValueError("prompt_template_path is required when mode='deepseek'")
        return generate_deepseek_report(summary, knowledge_items, prompt_template_path)

    structured = build_structured_result(summary, knowledge_items)
    return render_structured_result(structured)
