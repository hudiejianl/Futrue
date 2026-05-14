import torch
import torch.nn as nn


class ForceMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_classes: int = 4):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.reg_head = nn.Linear(hidden_dim, 1)
        self.cls_head = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        feat = self.backbone(x)
        return {
            "wear_reg": self.reg_head(feat),
            "wear_cls": self.cls_head(feat),
        }
