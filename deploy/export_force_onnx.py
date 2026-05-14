import argparse
from pathlib import Path

import torch

from src.models.force_mlp import ForceMLP


def parse_args():
    parser = argparse.ArgumentParser(description="Export Force-only model to ONNX.")
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\outputs\force_baseline_cls\best_model.pt"),
    )
    parser.add_argument(
        "--feature-file",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\force_cycle_features.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\deploy\force_only.onnx"),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    import pandas as pd

    feature_df = pd.read_csv(args.feature_file)
    feature_cols = [col for col in feature_df.columns if col not in {"cycle_id", "force_file"}]

    model = ForceMLP(input_dim=len(feature_cols))
    state = torch.load(args.model_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    dummy = torch.randn(1, len(feature_cols), dtype=torch.float32)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    class ExportWrapper(torch.nn.Module):
        def __init__(self, inner):
            super().__init__()
            self.inner = inner

        def forward(self, x):
            out = self.inner(x)
            return out["wear_reg"], out["wear_cls"]

    wrapper = ExportWrapper(model)

    torch.onnx.export(
        wrapper,
        dummy,
        str(args.output),
        input_names=["force_features"],
        output_names=["wear_reg", "wear_cls"],
        dynamic_axes={"force_features": {0: "batch"}, "wear_reg": {0: "batch"}, "wear_cls": {0: "batch"}},
        opset_version=17,
    )
    print(f"exported to {args.output}")


if __name__ == "__main__":
    main()
