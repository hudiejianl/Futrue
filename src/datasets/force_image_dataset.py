import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


def build_image_transform(train: bool):
    base = [
        transforms.Resize((224, 224)),
    ]
    if train:
        base.append(transforms.RandomHorizontalFlip(p=0.5))
    base.extend(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return transforms.Compose(base)


class ForceImageDataset(Dataset):
    def __init__(self, split_file: str, force_feature_file: str, train: bool, feature_mean=None, feature_std=None):
        split_df = pd.read_csv(split_file)
        force_df = pd.read_csv(force_feature_file)
        merged = split_df.merge(force_df, on=["cycle_id", "force_file"], how="left")
        feature_cols = [col for col in force_df.columns if col not in {"cycle_id", "force_file"}]
        merged = merged.dropna(subset=feature_cols).reset_index(drop=True)

        self.df = merged
        self.feature_cols = feature_cols
        self.feature_mean = feature_mean
        self.feature_std = feature_std
        self.image_transform = build_image_transform(train)

    def compute_feature_stats(self):
        mean = self.df[self.feature_cols].mean()
        std = self.df[self.feature_cols].std().replace(0, 1.0).fillna(1.0)
        return mean, std

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        feature_values = row[self.feature_cols].astype("float32")
        if self.feature_mean is not None and self.feature_std is not None:
            feature_values = (feature_values - self.feature_mean) / self.feature_std
        force_x = torch.tensor(feature_values.values.astype("float32"))

        image = Image.open(row["image_file"])
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = self.image_transform(image)

        wear_value = torch.tensor([float(row["wear_value"])], dtype=torch.float32)
        wear_level = torch.tensor(int(row["wear_level"]), dtype=torch.long)
        return {
            "force_features": force_x,
            "image": image,
            "wear_value": wear_value,
            "wear_level": wear_level,
            "meta": {
                "sample_id": row["sample_id"],
                "cycle_id": int(row["cycle_id"]),
                "cutting_edge": int(row["cutting_edge"]),
            },
        }
