import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


def build_image_transform(train: bool):
    ops = [transforms.Resize((224, 224))]
    if train:
        ops.append(transforms.RandomHorizontalFlip(p=0.5))
    ops.extend(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return transforms.Compose(ops)


class ToolWearMultimodalDataset(Dataset):
    def __init__(
        self,
        split_file: str,
        force_feature_file: str,
        vibration_feature_file: str | None = None,
        train: bool = True,
        feature_mean=None,
        feature_std=None,
        use_force: bool = True,
        use_vibration: bool = True,
        use_image: bool = True,
    ):
        split_df = pd.read_csv(split_file)
        merged = split_df.copy()

        self.use_force = use_force
        self.use_vibration = use_vibration
        self.use_image = use_image
        self.image_transform = build_image_transform(train)

        feature_cols = []
        if use_force:
            force_df = pd.read_csv(force_feature_file)
            merged = merged.merge(force_df, on=["cycle_id", "force_file"], how="left")
            feature_cols.extend([c for c in force_df.columns if c not in {"cycle_id", "force_file"}])

        if use_vibration and vibration_feature_file:
            vib_df = pd.read_csv(vibration_feature_file)
            merged = merged.merge(vib_df, on=["cycle_id", "vib_file"], how="left")
            feature_cols.extend([c for c in vib_df.columns if c not in {"cycle_id", "vib_file"}])

        if feature_cols:
            merged = merged.dropna(subset=feature_cols).reset_index(drop=True)

        if use_image:
            merged = merged[merged["image_file"].notna() & (merged["image_file"] != "")].reset_index(drop=True)

        self.df = merged
        self.feature_cols = feature_cols
        self.feature_mean = feature_mean
        self.feature_std = feature_std

    def compute_feature_stats(self):
        if not self.feature_cols:
            return None, None
        mean = self.df[self.feature_cols].mean()
        std = self.df[self.feature_cols].std().replace(0, 1.0).fillna(1.0)
        return mean, std

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        if self.feature_cols:
            values = row[self.feature_cols].astype("float32")
            if self.feature_mean is not None and self.feature_std is not None:
                values = (values - self.feature_mean) / self.feature_std
            feature_x = torch.tensor(values.values.astype("float32"))
        else:
            feature_x = torch.empty(0, dtype=torch.float32)

        if self.use_image:
            image = Image.open(row["image_file"])
            if image.mode != "RGB":
                image = image.convert("RGB")
            image = self.image_transform(image)
        else:
            image = torch.zeros(3, 224, 224, dtype=torch.float32)

        wear_value = torch.tensor([float(row["wear_value"])], dtype=torch.float32)
        wear_level = torch.tensor(int(row["wear_level"]), dtype=torch.long)

        return {
            "features": feature_x,
            "image": image,
            "wear_value": wear_value,
            "wear_level": wear_level,
            "meta": {
                "sample_id": row["sample_id"],
                "cycle_id": int(row["cycle_id"]),
                "cutting_edge": int(row["cutting_edge"]),
            },
        }
