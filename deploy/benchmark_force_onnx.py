import argparse
import json
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark ONNX Force-only model.")
    parser.add_argument(
        "--onnx-path",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\deploy\force_only.onnx"),
    )
    parser.add_argument(
        "--feature-file",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\force_cycle_features.csv"),
    )
    parser.add_argument("--runs", type=int, default=200)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\reports\force_onnx_benchmark.json"),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    feature_df = pd.read_csv(args.feature_file)
    feature_cols = [col for col in feature_df.columns if col not in {"cycle_id", "force_file"}]
    sample = feature_df.iloc[[0]][feature_cols].to_numpy(dtype=np.float32)

    session = ort.InferenceSession(str(args.onnx_path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    for _ in range(20):
        session.run(None, {input_name: sample})

    t0 = time.perf_counter()
    for _ in range(args.runs):
        session.run(None, {input_name: sample})
    elapsed = time.perf_counter() - t0

    avg_ms = elapsed / args.runs * 1000.0
    model_size_mb = args.onnx_path.stat().st_size / (1024 * 1024)

    report = {
        "onnx_path": str(args.onnx_path),
        "runs": args.runs,
        "avg_latency_ms": avg_ms,
        "model_size_mb": model_size_mb,
        "input_dim": len(feature_cols),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
