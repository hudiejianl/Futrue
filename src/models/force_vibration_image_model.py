import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small


class ForceVibrationImageModel(nn.Module):
    def __init__(self, feature_input_dim: int, hidden_dim: int = 64, num_classes: int = 4):
        super().__init__()
        self.feature_proj = nn.Sequential(
            nn.Linear(feature_input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
        )

        backbone = mobilenet_v3_small(weights=None)
        self.image_backbone = backbone.features
        self.image_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.image_proj = nn.Linear(576, 128)

        self.fusion = nn.Sequential(
            nn.Linear(64 + 128, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
        )
        self.reg_head = nn.Linear(64, 1)
        self.cls_head = nn.Linear(64, num_classes)

    def forward(self, feature_x, image):
        feat = self.feature_proj(feature_x)
        img = self.image_backbone(image)
        img = self.image_pool(img).flatten(1)
        img = self.image_proj(img)
        fused = self.fusion(torch.cat([feat, img], dim=1))
        return {
            "wear_reg": self.reg_head(fused),
            "wear_cls": self.cls_head(fused),
        }
