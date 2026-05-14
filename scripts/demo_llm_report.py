import argparse
import json
from pathlib import Path

import pandas as pd

from llm.report_generator import generate_report
from llm.retriever import KnowledgeRetriever
from llm.rule_engine import evaluate_rules


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a demo diagnostic report.")
    parser.add_argument(
        "--input-index",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\side_samples_complete.csv"),
    )
    parser.add_argument(
        "--kb-path",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\llm\knowledge_base.json"),
    )
    parser.add_argument("--sample-id", type=str, default="")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\reports\demo_report.txt"),
    )
    return parser.parse_args()


def build_summary(row: pd.Series) -> dict:
    return {
        "sample_id": row["sample_id"],
        "cycle_id": row["run_id"],
        "predicted_wear": float(row["wear_value"]),
        "wear_level": int(row["wear_level"]),
        "primary_model": "force_only",
        "use_image_context": True,
    }


def main():
    args = parse_args()
    df = pd.read_csv(args.input_index)
    if args.sample_id:
        row = df[df["sample_id"] == args.sample_id].iloc[0]
    else:
        row = df.sort_values("wear_value", ascending=False).iloc[0]

    summary = build_summary(row)
    rule_hits = evaluate_rules(summary)
    retriever = KnowledgeRetriever(str(args.kb_path))
    knowledge_items = retriever.retrieve(rule_hits)
    report = generate_report(summary, knowledge_items)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")

    payload = {
        "summary": summary,
        "rule_hits": rule_hits,
        "knowledge_items": knowledge_items,
        "report_path": str(args.output),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\n" + report)


if __name__ == "__main__":
    main()
