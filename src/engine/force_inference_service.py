from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import torch

from llm.report_generator import generate_report
from llm.retriever import KnowledgeRetriever
from llm.rule_engine import evaluate_rules
from src.models.force_mlp import ForceMLP


class ForceInferenceService:
    def __init__(
        self,
        split_file: str,
        train_split_file: str,
        feature_file: str,
        model_path: str,
        kb_path: str,
        prompt_template_path: str,
    ):
        self.split_file = Path(split_file)
        self.train_split_file = Path(train_split_file)
        self.feature_file = Path(feature_file)
        self.model_path = Path(model_path)
        self.kb_path = Path(kb_path)
        self.prompt_template_path = Path(prompt_template_path)

        self.split_df = pd.read_csv(self.split_file)
        self.feature_df = pd.read_csv(self.feature_file)
        self.feature_cols = [col for col in self.feature_df.columns if col not in {"cycle_id", "force_file"}]

        self.merged_df = self.split_df.merge(self.feature_df, on=["cycle_id", "force_file"], how="left")
        self.merged_df = self.merged_df.dropna(subset=self.feature_cols).reset_index(drop=True)

        train_df = pd.read_csv(self.train_split_file).merge(
            self.feature_df,
            on=["cycle_id", "force_file"],
            how="left",
        )
        train_df = train_df.dropna(subset=self.feature_cols).reset_index(drop=True)
        self.feature_mean = train_df[self.feature_cols].mean()
        self.feature_std = train_df[self.feature_cols].std().replace(0, 1.0).fillna(1.0)

        self.model = ForceMLP(input_dim=len(self.feature_cols))
        state = torch.load(self.model_path, map_location="cpu")
        self.model.load_state_dict(state)
        self.model.eval()

        self.retriever = KnowledgeRetriever(str(self.kb_path))

    def list_samples(self) -> list[str]:
        return self.merged_df["sample_id"].tolist()

    def _prepare_feature_tensor(self, row: pd.Series) -> torch.Tensor:
        values = row[self.feature_cols].astype("float32")
        values = (values - self.feature_mean) / self.feature_std
        return torch.tensor(values.values.astype("float32")).unsqueeze(0)

    def _build_summary(self, row: pd.Series, wear_pred: float, cls_pred: int) -> dict:
        return {
            "sample_id": row["sample_id"],
            "cycle_id": row["run_id"],
            "predicted_wear": wear_pred,
            "wear_level": cls_pred,
            "ground_truth_wear": float(row["wear_value"]),
            "ground_truth_level": int(row["wear_level"]),
            "primary_model": "force_only",
            "use_image_context": True,
            "image_file": row["image_file"],
        }

    def infer(self, sample_id: str, report_mode: str = "template") -> dict:
        row = self.merged_df[self.merged_df["sample_id"] == sample_id].iloc[0]
        x = self._prepare_feature_tensor(row)

        with torch.no_grad():
            out = self.model(x)
            wear_pred = float(out["wear_reg"].squeeze().item())
            cls_pred = int(out["wear_cls"].argmax(dim=1).item())

        summary = self._build_summary(row, wear_pred, cls_pred)
        rule_hits = evaluate_rules(summary)
        knowledge_items = self.retriever.retrieve(rule_hits, summary=summary)
        report = generate_report(
            summary,
            knowledge_items,
            mode=report_mode,
            prompt_template_path=str(self.prompt_template_path),
        )

        return {
            "summary": summary,
            "rule_hits": rule_hits,
            "knowledge_items": knowledge_items,
            "report": report,
        }
