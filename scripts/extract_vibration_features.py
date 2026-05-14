import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew


RAW_COLUMNS = [
    "time",
    "vib_x",
    "vib_y",
    "vib_z",
    "sound",
]

FEATURE_COLUMNS = ["vib_x", "vib_y", "vib_z", "sound"]


def parse_args():
    parser = argparse.ArgumentParser(description="Extract cycle-level vibration and sound features.")
    parser.add_argument(
        "--input-index",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\side_samples_complete.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed\index\vibration_cycle_features.csv"),
    )
    parser.add_argument("--chunksize", type=int, default=200000)
    parser.add_argument("--limit-cycles", type=int, default=0)
    parser.add_argument("--cycle-file", type=Path, default=None)
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
            "sum_fourth": 0.0,
            "sum_cube": 0.0,
            "energy_sum": 0.0,
        }
        for col in FEATURE_COLUMNS
    }


def update_stats(stats, chunk):
    for src_col, col in zip(chunk.columns[1:], FEATURE_COLUMNS):
        arr = pd.to_numeric(chunk[src_col], errors="coerce").dropna().to_numpy(dtype=np.float64)
        if arr.size == 0:
            continue
        col_stats = stats[col]
        col_stats["count"] += int(arr.size)
        col_stats["sum"] += float(arr.sum())
        col_stats["sum_sq"] += float(np.square(arr).sum())
        col_stats["min"] = min(col_stats["min"], float(arr.min()))
        col_stats["max"] = max(col_stats["max"], float(arr.max()))
        col_stats["abs_sum"] += float(np.abs(arr).sum())
        col_stats["sum_fourth"] += float(np.power(arr, 4).sum())
        col_stats["sum_cube"] += float(np.power(arr, 3).sum())
        col_stats["energy_sum"] += float(np.square(arr).sum())


def finalize_stats(stats):
    row = {}
    for col in FEATURE_COLUMNS:
        item = stats[col]
        count = max(item["count"], 1)
        mean = item["sum"] / count
        variance = max(item["sum_sq"] / count - mean * mean, 0.0)
        std = variance ** 0.5
        row[f"{col}_mean"] = mean
        row[f"{col}_std"] = std
        row[f"{col}_min"] = item["min"] if item["min"] != float("inf") else np.nan
        row[f"{col}_max"] = item["max"] if item["max"] != float("-inf") else np.nan
        row[f"{col}_abs_mean"] = item["abs_sum"] / count
        row[f"{col}_rms"] = (item["energy_sum"] / count) ** 0.5
        row[f"{col}_peak_to_peak"] = row[f"{col}_max"] - row[f"{col}_min"]
        centered_m2 = variance
        centered_m3 = item["sum_cube"] / count
        centered_m4 = item["sum_fourth"] / count
        if std > 1e-12:
            row[f"{col}_skew_approx"] = centered_m3 / (std ** 3)
            row[f"{col}_kurtosis_approx"] = centered_m4 / (std ** 4)
        else:
            row[f"{col}_skew_approx"] = 0.0
            row[f"{col}_kurtosis_approx"] = 0.0
    return row


def extract_csv_features(file_path: Path, chunksize: int):
    stats = init_stats()
    reader = pd.read_csv(file_path, chunksize=chunksize, encoding="utf-8", encoding_errors="ignore")
    for chunk in reader:
        update_stats(stats, chunk)
    return finalize_stats(stats)


def extract_excel_features(file_path: Path):
    stats = init_stats()
    excel = pd.ExcelFile(file_path)
    for sheet_name in excel.sheet_names:
        df = excel.parse(sheet_name)
        if df.shape[1] < 5:
            continue
        update_stats(stats, df.iloc[:, :5])
    return finalize_stats(stats)


def extract_file_features(file_path: Path, chunksize: int):
    if file_path.suffix.lower() == ".csv":
        return extract_csv_features(file_path, chunksize)
    if file_path.suffix.lower() == ".xlsx":
        return extract_excel_features(file_path)
    raise ValueError(f"Unsupported file type: {file_path}")


def main():
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    index_df = pd.read_csv(args.input_index)
    cycle_files = (
        index_df[["cycle_id", "vib_file"]]
        .drop_duplicates(subset=["cycle_id"])
        .sort_values("cycle_id")
    )
    if args.cycle_file is not None:
        keep_cycles = {
            int(x.strip())
            for x in args.cycle_file.read_text(encoding="utf-8").splitlines()
            if x.strip()
        }
        cycle_files = cycle_files[cycle_files["cycle_id"].isin(sorted(keep_cycles))].copy()
    if args.limit_cycles > 0:
        cycle_files = cycle_files.head(args.limit_cycles).copy()

    rows = []
    failed_files = []
    for item in cycle_files.itertuples(index=False):
        cycle_id = int(item.cycle_id)
        vib_file = Path(item.vib_file)
        try:
            features = extract_file_features(vib_file, args.chunksize)
            features["cycle_id"] = cycle_id
            features["vib_file"] = str(vib_file)
            rows.append(features)
            print(f"processed cycle {cycle_id:02d}")
        except Exception as e:
            failed_files.append({"cycle_id": cycle_id, "vib_file": str(vib_file), "error": repr(e)})
            print(f"failed cycle {cycle_id:02d}: {vib_file.name} -> {e!r}")

    feature_df = pd.DataFrame(rows).sort_values("cycle_id")
    feature_df.to_csv(args.output, index=False)

    report = {
        "num_cycles": int(len(feature_df)),
        "feature_columns": [col for col in feature_df.columns if col not in {"cycle_id", "vib_file"}],
        "failed_files": failed_files,
    }
    with args.output.with_suffix(".json").open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
