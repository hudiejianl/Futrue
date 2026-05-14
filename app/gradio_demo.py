import json
import subprocess
from pathlib import Path

import gradio as gr
import pandas as pd


ROOT = Path(r"D:\my\Future\toolwear_multimodal")
VAL_FILE = ROOT / "data" / "processed" / "splits" / "val.csv"
SCRIPT = ROOT / "scripts" / "infer_force_and_report.py"
REPORT_PATH = ROOT / "reports" / "force_infer_report.txt"


def list_samples():
    df = pd.read_csv(VAL_FILE)
    return df["sample_id"].tolist()


def run_inference(sample_id: str):
    cmd = [
        "python",
        str(SCRIPT),
        "--sample-id",
        sample_id,
        "--output",
        str(REPORT_PATH),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"推理失败：\n{result.stderr}", ""

    text = REPORT_PATH.read_text(encoding="utf-8") if REPORT_PATH.exists() else ""
    return result.stdout, text


def build_demo():
    sample_choices = list_samples()
    with gr.Blocks(title="Tool Wear Demo") as demo:
        gr.Markdown("# Tool Wear Monitoring Demo")
        sample_id = gr.Dropdown(choices=sample_choices, label="选择样本", value=sample_choices[0] if sample_choices else None)
        run_btn = gr.Button("运行推理")
        raw_output = gr.Textbox(label="结构化输出", lines=20)
        report_output = gr.Textbox(label="诊断报告", lines=16)
        run_btn.click(fn=run_inference, inputs=[sample_id], outputs=[raw_output, report_output])
    return demo


if __name__ == "__main__":
    demo = build_demo()
    demo.launch()
