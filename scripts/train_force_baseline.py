import argparse
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score, mean_absolute_error, mean_squared_error, r2_score
from torch.utils.data import DataLoader

from src.datasets.force_feature_dataset import ForceFeatureDataset
from src.models.force_mlp import ForceMLP


def parse_args():
    parser = argparse.ArgumentParser(description="Train force-only baseline.")
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\data\processed"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(r"D:\my\Future\toolwear_multimodal\outputs\force_baseline"),
    )
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--reg-weight", type=float, default=1.0)
    parser.add_argument("--cls-weight", type=float, default=0.8)
    parser.add_argument("--select-metric", type=str, default="rmse", choices=["rmse", "f1_macro"])
    return parser.parse_args()


def evaluate(model, loader, device, reg_weight, cls_weight):
    model.eval()
    reg_preds, reg_targets = [], []
    cls_preds, cls_targets = [], []
    total_loss = 0.0
    with torch.no_grad():
        for batch in loader:
            x = batch["features"].to(device)
            y_reg = batch["wear_value"].to(device)
            y_cls = batch["wear_level"].to(device)
            out = model(x)
            reg_loss = F.mse_loss(out["wear_reg"], y_reg)
            cls_loss = F.cross_entropy(out["wear_cls"], y_cls)
            loss = reg_weight * reg_loss + cls_weight * cls_loss
            total_loss += loss.item() * x.size(0)

            reg_preds.extend(out["wear_reg"].squeeze(1).cpu().tolist())
            reg_targets.extend(y_reg.squeeze(1).cpu().tolist())
            cls_preds.extend(out["wear_cls"].argmax(dim=1).cpu().tolist())
            cls_targets.extend(y_cls.cpu().tolist())

    rmse = mean_squared_error(reg_targets, reg_preds) ** 0.5
    return {
        "loss": total_loss / max(len(loader.dataset), 1),
        "mae": mean_absolute_error(reg_targets, reg_preds),
        "rmse": rmse,
        "r2": r2_score(reg_targets, reg_preds),
        "f1_macro": f1_score(cls_targets, cls_preds, average="macro"),
    }


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    feature_file = args.data_root / "index" / "force_cycle_features.csv"
    train_file = args.data_root / "splits" / "train.csv"
    val_file = args.data_root / "splits" / "val.csv"

    train_ds = ForceFeatureDataset(str(train_file), str(feature_file))
    feature_mean, feature_std = train_ds.compute_feature_stats()
    train_ds = ForceFeatureDataset(str(train_file), str(feature_file), feature_mean=feature_mean, feature_std=feature_std)
    val_ds = ForceFeatureDataset(str(val_file), str(feature_file), feature_mean=feature_mean, feature_std=feature_std)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    model = ForceMLP(input_dim=len(train_ds.feature_cols)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    history = []
    best = None
    best_state = None

    for epoch in range(1, args.epochs + 1):
        model.train()
        for batch in train_loader:
            x = batch["features"].to(device)
            y_reg = batch["wear_value"].to(device)
            y_cls = batch["wear_level"].to(device)

            out = model(x)
            reg_loss = F.mse_loss(out["wear_reg"], y_reg)
            cls_loss = F.cross_entropy(out["wear_cls"], y_cls)
            loss = args.reg_weight * reg_loss + args.cls_weight * cls_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        train_metrics = evaluate(model, train_loader, device, args.reg_weight, args.cls_weight)
        val_metrics = evaluate(model, val_loader, device, args.reg_weight, args.cls_weight)
        record = {
            "epoch": epoch,
            "train": train_metrics,
            "val": val_metrics,
        }
        history.append(record)
        print(json.dumps(record, ensure_ascii=False))

        if best is None:
            better = True
        elif args.select_metric == "rmse":
            better = val_metrics["rmse"] < best["rmse"]
        else:
            better = val_metrics["f1_macro"] > best["f1_macro"]
        if better:
            best = val_metrics
            best_state = model.state_dict()

    torch.save(best_state, args.output_dir / "best_model.pt")
    with (args.output_dir / "history.json").open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    with (args.output_dir / "best_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(best, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
