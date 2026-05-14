import argparse
from pathlib import Path

import pandas as pd

from src.engine.force_inference_service import ForceInferenceService
from src.utils.env_loader import load_env_file


def parse_args():
    parser = argparse.ArgumentParser(description="Compare template and deepseek reports.")
    parser.add_argument(
        "--split-file",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\splits\val.csv"),
    )
    parser.add_argument(
        "--train-split-file",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\splits\train.csv"),
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
        "--prompt-template",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\llm\prompt_template.txt"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\reports\report_mode_comparison.md"),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    load_env_file(Path(r"D:\my\Future\toolwear_multimodal\.env"))

    df = pd.read_csv(args.split_file)
    low_sample = df.sort_values("wear_value", ascending=True).iloc[0]["sample_id"]
    high_sample = df.sort_values("wear_value", ascending=False).iloc[0]["sample_id"]

    service = ForceInferenceService(
        split_file=str(args.split_file),
        train_split_file=str(args.train_split_file),
        feature_file=str(args.feature_file),
        model_path=str(args.model_path),
        kb_path=str(args.kb_path),
        prompt_template_path=str(args.prompt_template),
    )

    sections = ["# Report Mode Comparison", ""]
    for sample_id in [low_sample, high_sample]:
        template_result = service.infer(sample_id=sample_id, report_mode="template")
        deepseek_result = service.infer(sample_id=sample_id, report_mode="deepseek")

        sections.extend(
            [
                f"## Sample: {sample_id}",
                "",
                "### Summary",
                "```json",
                str(template_result["summary"]).replace("'", '"'),
                "```",
                "",
                "### Template Report",
                "```text",
                template_result["report"],
                "```",
                "",
                "### DeepSeek Report",
                "```text",
                deepseek_result["report"],
                "```",
                "",
            ]
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(sections), encoding="utf-8")
    print(f"written to {args.output}")


if __name__ == "__main__":
    main()
