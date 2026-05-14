import argparse
import json
from pathlib import Path

from src.engine.force_inference_service import ForceInferenceService
from src.utils.env_loader import load_env_file


def parse_args():
    parser = argparse.ArgumentParser(description="Run force model inference and generate report.")
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
        "--report-mode",
        type=str,
        default="template",
        choices=["template", "openai", "deepseek"],
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


def main():
    args = parse_args()
    load_env_file(Path(r"D:\my\Future\toolwear_multimodal\.env"))
    service = ForceInferenceService(
        split_file=str(args.split_file),
        train_split_file=str(args.train_split_file),
        feature_file=str(args.feature_file),
        model_path=str(args.model_path),
        kb_path=str(args.kb_path),
        prompt_template_path=str(args.prompt_template),
    )

    sample_id = args.sample_id or service.list_samples()[0]
    result = service.infer(sample_id=sample_id, report_mode=args.report_mode)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result["report"], encoding="utf-8")

    payload = {
        "summary": result["summary"],
        "rule_hits": result["rule_hits"],
        "knowledge_items": result["knowledge_items"],
        "report_path": str(args.output),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\n" + result["report"])


if __name__ == "__main__":
    main()
