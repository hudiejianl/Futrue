import json
from pathlib import Path

import gradio as gr

from src.engine.force_inference_service import ForceInferenceService
from src.utils.env_loader import load_env_file


ROOT = Path(r"D:\my\Future\toolwear_multimodal")
load_env_file(ROOT / ".env")

SERVICE = ForceInferenceService(
    split_file=str(ROOT / "data" / "processed" / "splits" / "val.csv"),
    train_split_file=str(ROOT / "data" / "processed" / "splits" / "train.csv"),
    feature_file=str(ROOT / "data" / "processed" / "index" / "force_cycle_features.csv"),
    model_path=str(ROOT / "outputs" / "force_baseline_cls" / "best_model.pt"),
    kb_path=str(ROOT / "llm" / "knowledge_base.json"),
    prompt_template_path=str(ROOT / "llm" / "prompt_template.txt"),
)

BENCHMARK = json.loads((ROOT / "reports" / "force_onnx_benchmark.json").read_text(encoding="utf-8"))


def run_inference(sample_id: str, report_mode: str):
    result = SERVICE.infer(sample_id=sample_id, report_mode=report_mode)
    summary_text = json.dumps(result["summary"], ensure_ascii=False, indent=2)
    rule_text = json.dumps(result["rule_hits"], ensure_ascii=False, indent=2)
    knowledge_text = json.dumps(result["knowledge_items"], ensure_ascii=False, indent=2)
    image_path = result["summary"].get("image_file", "")
    benchmark_text = json.dumps(BENCHMARK, ensure_ascii=False, indent=2)
    return image_path, summary_text, rule_text, knowledge_text, result["report"], benchmark_text


def build_demo():
    samples = SERVICE.list_samples()
    with gr.Blocks(title="Tool Wear Monitoring System") as demo:
        gr.Markdown("# Tool Wear Monitoring System")
        gr.Markdown(
            "Force-only prediction backbone + multimodal auxiliary context + explanation module + ONNX deployment."
        )
        gr.Markdown(
            "Recommended demo mode: `deepseek`. "
            "Use `template` as a deterministic fallback when external API output is not needed."
        )

        with gr.Row():
            sample_id = gr.Dropdown(
                choices=samples,
                label="Select Sample",
                value=samples[0] if samples else None,
            )
            report_mode = gr.Dropdown(
                choices=["template", "deepseek", "openai"],
                value="template",
                label="Report Backend",
            )
            run_btn = gr.Button("Run Inference")

        with gr.Row():
            image_view = gr.Image(label="Tool Image", type="filepath")
            report_output = gr.Textbox(label="Diagnostic Report", lines=18)

        with gr.Row():
            summary_output = gr.Textbox(label="Prediction Summary", lines=14)
            rule_output = gr.Textbox(label="Rule Hits", lines=14)

        with gr.Row():
            knowledge_output = gr.Textbox(label="Knowledge Items", lines=14)
            benchmark_output = gr.Textbox(label="Deployment Benchmark", lines=14)

        gr.Markdown(
            "Explanation panels: `Prediction Summary` shows model output, "
            "`Rule Hits` shows matched deterministic rules, "
            "`Knowledge Items` shows retrieved evidence, and "
            "`Diagnostic Report` shows the final rendered explanation."
        )

        run_btn.click(
            fn=run_inference,
            inputs=[sample_id, report_mode],
            outputs=[image_view, summary_output, rule_output, knowledge_output, report_output, benchmark_output],
        )

    return demo


if __name__ == "__main__":
    build_demo().launch()
