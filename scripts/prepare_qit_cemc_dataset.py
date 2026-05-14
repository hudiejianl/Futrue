import argparse
import json
import random
import re
from pathlib import Path

import pandas as pd


SIDE_LABELS = [
    ("side", 1, "vbmax", 1),
    ("side", 1, "vb_half_ap", 2),
    ("side", 1, "wear_area", 3),
    ("side", 2, "vbmax", 4),
    ("side", 2, "vb_half_ap", 5),
    ("side", 2, "wear_area", 6),
    ("side", 3, "vbmax", 7),
    ("side", 3, "vb_half_ap", 8),
    ("side", 3, "wear_area", 9),
    ("side", 4, "vbmax", 10),
    ("side", 4, "vb_half_ap", 11),
    ("side", 4, "wear_area", 12),
]

END_LABELS = [
    ("end", 1, "vbmax", 13),
    ("end", 1, "wear_area", 14),
    ("end", 2, "vbmax", 15),
    ("end", 2, "wear_area", 16),
    ("end", 3, "vbmax", 17),
    ("end", 3, "wear_area", 18),
    ("end", 4, "vbmax", 19),
    ("end", 4, "wear_area", 20),
]


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare QIT-CEMC dataset indices.")
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=Path(r"D:\my\Future\QIT-CEMC Dataset"),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed"),
    )
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def normalize_sensor_suffix(value: str) -> str:
    return value.zfill(2)


def build_sensor_maps(dataset_root: Path):
    force_dir = dataset_root / "Force and torque data"
    vib_dir = dataset_root / "Vibration and sound data"
    image_dir = dataset_root / "Image"

    force_files = sorted(force_dir.glob("*.txt"), key=lambda p: p.name)
    force_map = {idx: str(path) for idx, path in enumerate(force_files, start=1)}

    vib_files = sorted(
        [p for p in vib_dir.iterdir() if p.suffix.lower() in {".csv", ".xlsx"}],
        key=lambda p: p.name,
    )
    vib_map = {}
    vib_cycle_ids = [1] + list(range(3, 69))
    for cycle_id, path in zip(vib_cycle_ids, vib_files):
        vib_map[cycle_id] = str(path)

    image_map = {}
    for path in sorted(image_dir.iterdir(), key=lambda p: int(p.name)):
        if not path.is_dir():
            continue
        cycle_id = int(path.name)
        files = sorted([x for x in path.iterdir() if x.is_file()])
        image_map[cycle_id] = {
            "dir": str(path),
            "files": [str(x) for x in files],
            "count": len(files),
        }

    return force_map, vib_map, image_map


def parse_tool_wear_xls(xls_path: Path):
    raw = pd.read_excel(xls_path, header=None)
    data = raw.iloc[4:].copy().reset_index(drop=True)
    data.rename(columns={0: "cycle_id"}, inplace=True)
    data["cycle_id"] = pd.to_numeric(data["cycle_id"], errors="coerce")
    data = data.dropna(subset=["cycle_id"]).copy()
    data["cycle_id"] = data["cycle_id"].astype(int)

    side_rows = []
    end_rows = []

    for _, row in data.iterrows():
        cycle_id = int(row["cycle_id"])
        for tooth_type, edge_id, metric_name, col_idx in SIDE_LABELS:
            value = pd.to_numeric(row[col_idx], errors="coerce")
            side_rows.append(
                {
                    "cycle_id": cycle_id,
                    "tooth_type": tooth_type,
                    "cutting_edge": edge_id,
                    "metric_name": metric_name,
                    "metric_value": value,
                }
            )
        for tooth_type, edge_id, metric_name, col_idx in END_LABELS:
            value = pd.to_numeric(row[col_idx], errors="coerce")
            end_rows.append(
                {
                    "cycle_id": cycle_id,
                    "tooth_type": tooth_type,
                    "cutting_edge": edge_id,
                    "metric_name": metric_name,
                    "metric_value": value,
                }
            )

    side_df = pd.DataFrame(side_rows)
    end_df = pd.DataFrame(end_rows)
    return side_df, end_df


def make_side_label_table(side_long: pd.DataFrame):
    pivot = (
        side_long.pivot_table(
            index=["cycle_id", "cutting_edge"],
            columns="metric_name",
            values="metric_value",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    pivot["image_file"] = pivot.apply(
        lambda r: f"{int(r['cycle_id']):02d}/side-{int(r['cutting_edge'])}.png", axis=1
    )
    pivot["wear_value"] = pivot["vbmax"]
    pivot["wear_level"] = pd.cut(
        pivot["wear_value"],
        bins=[-float("inf"), 0.10, 0.20, 0.30, float("inf")],
        labels=[0, 1, 2, 3],
    ).astype(int)
    return pivot


def make_end_label_table(end_long: pd.DataFrame):
    pivot = (
        end_long.pivot_table(
            index=["cycle_id", "cutting_edge"],
            columns="metric_name",
            values="metric_value",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    pivot["image_file"] = pivot.apply(
        lambda r: f"{int(r['cycle_id']):02d}/end-{int(r['cutting_edge'])}.png", axis=1
    )
    pivot["wear_value"] = pivot["vbmax"]
    pivot["wear_level"] = pd.cut(
        pivot["wear_value"],
        bins=[-float("inf"), 0.10, 0.20, 0.30, float("inf")],
        labels=[0, 1, 2, 3],
    ).astype(int)
    return pivot


def build_side_samples(side_table: pd.DataFrame, dataset_root: Path, force_map, vib_map, image_map):
    rows = []
    for _, row in side_table.iterrows():
        cycle_id = int(row["cycle_id"])
        image_rel = row["image_file"]
        image_path = dataset_root / "Image" / image_rel
        has_force = cycle_id in force_map
        has_vib = cycle_id in vib_map
        has_image = image_path.exists()

        rows.append(
            {
                "sample_id": f"cycle_{cycle_id:02d}_side_{int(row['cutting_edge'])}",
                "run_id": f"cycle_{cycle_id:02d}",
                "cycle_id": cycle_id,
                "tooth_type": "side",
                "cutting_edge": int(row["cutting_edge"]),
                "force_file": force_map.get(cycle_id, ""),
                "vib_file": vib_map.get(cycle_id, ""),
                "image_file": str(image_path) if has_image else "",
                "image_rel": image_rel,
                "wear_value": float(row["wear_value"]) if pd.notna(row["wear_value"]) else None,
                "wear_level": int(row["wear_level"]) if pd.notna(row["wear_level"]) else None,
                "vb_half_ap": float(row["vb_half_ap"]) if pd.notna(row.get("vb_half_ap")) else None,
                "wear_area": float(row["wear_area"]) if pd.notna(row.get("wear_area")) else None,
                "has_force": has_force,
                "has_vib": has_vib,
                "has_image": has_image,
                "is_complete_multimodal": has_force and has_vib and has_image,
                "image_dir_count": image_map.get(cycle_id, {}).get("count", 0),
                "remark": "" if has_image else "missing_image",
            }
        )
    return pd.DataFrame(rows)


def split_cycles(cycle_ids, seed):
    cycle_ids = sorted(cycle_ids)
    rng = random.Random(seed)
    rng.shuffle(cycle_ids)

    n = len(cycle_ids)
    n_train = int(n * 0.7)
    n_val = int(n * 0.15)

    train = cycle_ids[:n_train]
    val = cycle_ids[n_train:n_train + n_val]
    test = cycle_ids[n_train + n_val:]
    return train, val, test


def write_split(df: pd.DataFrame, train_cycles, val_cycles, test_cycles, split_dir: Path):
    split_dir.mkdir(parents=True, exist_ok=True)
    train_df = df[df["cycle_id"].isin(train_cycles)].copy()
    val_df = df[df["cycle_id"].isin(val_cycles)].copy()
    test_df = df[df["cycle_id"].isin(test_cycles)].copy()

    train_df.to_csv(split_dir / "train.csv", index=False)
    val_df.to_csv(split_dir / "val.csv", index=False)
    test_df.to_csv(split_dir / "test.csv", index=False)

    report = {
        "train_cycles": train_cycles,
        "val_cycles": val_cycles,
        "test_cycles": test_cycles,
        "num_samples": {
            "train": int(len(train_df)),
            "val": int(len(val_df)),
            "test": int(len(test_df)),
        },
        "wear_level_distribution": {
            "train": train_df["wear_level"].value_counts().sort_index().to_dict(),
            "val": val_df["wear_level"].value_counts().sort_index().to_dict(),
            "test": test_df["wear_level"].value_counts().sort_index().to_dict(),
        },
    }
    with (split_dir / "split_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()
    output_root = args.output_root
    labels_dir = output_root / "labels"
    index_dir = output_root / "index"
    splits_dir = output_root / "splits"
    labels_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)
    splits_dir.mkdir(parents=True, exist_ok=True)

    force_map, vib_map, image_map = build_sensor_maps(args.dataset_root)
    side_long, end_long = parse_tool_wear_xls(args.dataset_root / "tool wear.xls")

    side_long.to_csv(labels_dir / "tool_wear_side_long.csv", index=False)
    end_long.to_csv(labels_dir / "tool_wear_end_long.csv", index=False)

    side_table = make_side_label_table(side_long)
    end_table = make_end_label_table(end_long)
    side_table.to_csv(labels_dir / "tool_wear_side_table.csv", index=False)
    end_table.to_csv(labels_dir / "tool_wear_end_table.csv", index=False)

    side_samples = build_side_samples(side_table, args.dataset_root, force_map, vib_map, image_map)
    side_samples.to_csv(index_dir / "side_samples_all.csv", index=False)

    complete_side_samples = side_samples[side_samples["is_complete_multimodal"]].copy()
    complete_side_samples.to_csv(index_dir / "side_samples_complete.csv", index=False)

    train_cycles, val_cycles, test_cycles = split_cycles(
        sorted(complete_side_samples["cycle_id"].unique().tolist()),
        args.seed,
    )
    write_split(complete_side_samples, train_cycles, val_cycles, test_cycles, splits_dir)

    report = {
        "dataset_root": str(args.dataset_root),
        "force_files": len(force_map),
        "vibration_files": len(vib_map),
        "image_dirs": len(image_map),
        "side_label_rows": int(len(side_table)),
        "end_label_rows": int(len(end_table)),
        "side_samples_all": int(len(side_samples)),
        "side_samples_complete": int(len(complete_side_samples)),
        "missing_vibration_cycles": sorted(set(force_map) - set(vib_map)),
        "incomplete_image_samples": int((~side_samples["has_image"]).sum()),
    }
    with (output_root / "prepare_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
