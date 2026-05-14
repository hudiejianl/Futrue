import argparse
import json
from pathlib import Path

import pandas as pd
import torch

from llm.report_generator import generate_report
from llm.retriever import KnowledgeRetriever
from llm.rule_engine import evaluate_rules
from src.models.force_mlp import ForceMLP


def parse_args():
    parser = argparse.ArgumentParser(description="Run force model inference and generate report.")
    parser.add_argument(
        "--split-file",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\splits\val.csv"),
    )
    parser.add_argument(
        "--feature-file",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\force_cycle_features.csv"),
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\outputs\force_baseline_cls\best_model.pt"),
    )
    parser.add_argument(
        "--kb-path",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\llm\knowledge_base.json"),
    )
    parser.add_argument(
        "--report-mode",
        type=str,
        default="template",
        choices=["template", "openai"],
    )
    parser.add_argument(
        "--prompt-template",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\llm\prompt_template.txt"),
    )
    parser.add_argument("--sample-id", type=str, default="")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\reports\force_infer_report.txt"),
    )
    return parser.parse_args()


def prepare_row(split_file: Path, feature_file: Path, sample_id: str):
    split_df = pd.read_csv(split_file)
    feature_df = pd.read_csv(feature_file)
    merged = split_df.merge(feature_df, on=["cycle_id", "force_file"], how="left")
    feature_cols = [col for col in feature_df.columns if col not in {"cycle_id", "force_file"}]
    merged = merged.dropna(subset=feature_cols).reset_index(drop=True)

    if sample_id:
        row = merged[merged["sample_id"] == sample_id].iloc[0]
    else:
        row = merged.sort_values("wear_value", ascending=False).iloc[0]

    train_df = pd.read_csv(Path(r"D:\my\Future\toolwear_multimodal\data\processed\splits\train.csv")).merge(
        feature_df,
        on=["cycle_id", "force_file"],
        how="left",
    ).dropna(subset=feature_cols).reset_index(drop=True)
    mean = train_df[feature_cols].mean()
    std = train_df[feature_cols].std().replace(0, 1.0).fillna(1.0)

    values = row[feature_cols].astype("float32")
    values = (values - mean) / std
    x = torch.tensor(values.values.astype("float32")).unsqueeze(0)
    return row, feature_cols, x


def build_summary(row: pd.Series, wear_pred: float, cls_pred: int) -> dict:
    return {
        "sample_id": row["sample_id"],
        "cycle_id": row["run_id"],
        "predicted_wear": wear_pred,
        "wear_level": cls_pred,
        "ground_truth_wear": float(row["wear_value"]),
        "ground_truth_level": int(row["wear_level"]),
        "primary_model": "force_only",
        "use_image_context": True,
    }


def main():
    args = parse_args()
    row, feature_cols, x = prepare_row(args.split_file, args.feature_file, args.sample_id)

    model = ForceMLP(input_dim=len(feature_cols))
    state = torch.load(args.model_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    with torch.no_grad():
        out = model(x)
        wear_pred = float(out["wear_reg"].squeeze().item())
        cls_pred = int(out["wear_cls"].argmax(dim=1).item())

    summary = build_summary(row, wear_pred, cls_pred)
    rule_hits = evaluate_rules(summary)
    retriever = KnowledgeRetriever(str(args.kb_path))
    knowledge_items = retriever.retrieve(rule_hits)
    report = generate_report(
        summary,
        knowledge_items,
        mode=args.report_mode,
        prompt_template_path=str(args.prompt_template),
    )

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
