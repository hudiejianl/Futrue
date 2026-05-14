import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


FEATURE_COLUMNS = ["Fx", "Fy", "Fz", "Mz"]


def parse_args():
    parser = argparse.ArgumentParser(description="Extract cycle-level force features.")
    parser.add_argument(
        "--input-index",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\side_samples_complete.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\force_cycle_features.csv"),
    )
    parser.add_argument("--chunksize", type=int, default=200000)
    parser.add_argument("--limit-cycles", type=int, default=0)
    return parser.parse_args()


def init_stats():
    return {
        col: {
            "count": 0,
            "sum": 0.0,
            "sum_sq": 0.0,
            "min": float("inf"),
            "max": float("-inf"),
            "abs_sum": 0.0,
        }
        for col in FEATURE_COLUMNS
    }


def update_stats(stats, chunk):
    for col in FEATURE_COLUMNS:
        arr = pd.to_numeric(chunk[col], errors="coerce").dropna().to_numpy(dtype=np.float64)
        if arr.size == 0:
            continue
        col_stats = stats[col]
        col_stats["count"] += int(arr.size)
        col_stats["sum"] += float(arr.sum())
        col_stats["sum_sq"] += float(np.square(arr).sum())
        col_stats["min"] = min(col_stats["min"], float(arr.min()))
        col_stats["max"] = max(col_stats["max"], float(arr.max()))
        col_stats["abs_sum"] += float(np.abs(arr).sum())


def finalize_stats(stats):
    row = {}
    for col in FEATURE_COLUMNS:
        item = stats[col]
        count = max(item["count"], 1)
        mean = item["sum"] / count
        variance = max(item["sum_sq"] / count - mean * mean, 0.0)
        std = variance ** 0.5
        row[f"{col.lower()}_mean"] = mean
        row[f"{col.lower()}_std"] = std
        row[f"{col.lower()}_min"] = item["min"] if item["min"] != float("inf") else np.nan
        row[f"{col.lower()}_max"] = item["max"] if item["max"] != float("-inf") else np.nan
        row[f"{col.lower()}_abs_mean"] = item["abs_sum"] / count
    return row


def extract_file_features(file_path: Path, chunksize: int):
    stats = init_stats()
    reader = pd.read_csv(file_path, sep="\t", chunksize=chunksize)
    for chunk in reader:
        chunk.columns = ["Time", "Fx", "Fy", "Fz", "Mz"]
        update_stats(stats, chunk)
    return finalize_stats(stats)


def main():
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    index_df = pd.read_csv(args.input_index)
    cycle_files = (
        index_df[["cycle_id", "force_file"]]
        .drop_duplicates(subset=["cycle_id"])
        .sort_values("cycle_id")
    )
    if args.limit_cycles > 0:
        cycle_files = cycle_files.head(args.limit_cycles).copy()

    rows = []
    for item in cycle_files.itertuples(index=False):
        cycle_id = int(item.cycle_id)
        force_file = Path(item.force_file)
        features = extract_file_features(force_file, args.chunksize)
        features["cycle_id"] = cycle_id
        features["force_file"] = str(force_file)
        rows.append(features)
        print(f"processed cycle {cycle_id:02d}")

    feature_df = pd.DataFrame(rows).sort_values("cycle_id")
    feature_df.to_csv(args.output, index=False)

    report = {
        "num_cycles": int(len(feature_df)),
        "feature_columns": [col for col in feature_df.columns if col not in {"cycle_id", "force_file"}],
    }
    with args.output.with_suffix(".json").open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
