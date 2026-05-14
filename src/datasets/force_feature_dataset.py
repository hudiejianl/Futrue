from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import Dataset


class ForceFeatureDataset(Dataset):
    def __init__(self, split_file: str, feature_file: str, feature_mean=None, feature_std=None):
        self.split_df = pd.read_csv(split_file)
        self.feature_df = pd.read_csv(feature_file)

        merged = self.split_df.merge(self.feature_df, on=["cycle_id", "force_file"], how="left")
        merged = merged.dropna(subset=[col for col in self.feature_df.columns if col not in {"cycle_id", "force_file"}])
        self.df = merged.reset_index(drop=True)

        self.feature_cols = [col for col in self.feature_df.columns if col not in {"cycle_id", "force_file"}]
        self.feature_mean = feature_mean
        self.feature_std = feature_std

    def compute_feature_stats(self):
        mean = self.df[self.feature_cols].mean()
        std = self.df[self.feature_cols].std().replace(0, 1.0).fillna(1.0)
        return mean, std

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        values = row[self.feature_cols].astype("float32")
        if self.feature_mean is not None and self.feature_std is not None:
            values = (values - self.feature_mean) / self.feature_std
        x = torch.tensor(values.values.astype("float32"))
        wear_value = torch.tensor([float(row["wear_value"])], dtype=torch.float32)
        wear_level = torch.tensor(int(row["wear_level"]), dtype=torch.long)
        return {
            "features": x,
            "wear_value": wear_value,
            "wear_level": wear_level,
            "meta": {
                "sample_id": row["sample_id"],
                "cycle_id": int(row["cycle_id"]),
                "cutting_edge": int(row["cutting_edge"]),
            },
        }
