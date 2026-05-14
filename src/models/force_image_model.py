import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small


class ForceImageModel(nn.Module):
    def __init__(self, force_input_dim: int, hidden_dim: int = 64, num_classes: int = 4):
        super().__init__()
        backbone = mobilenet_v3_small(weights=None)
        self.image_backbone = backbone.features
        self.image_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.image_proj = nn.Linear(576, 128)

        self.force_proj = nn.Sequential(
            nn.Linear(force_input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
        )

        self.fusion = nn.Sequential(
            nn.Linear(128 + 64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
        )
        self.reg_head = nn.Linear(64, 1)
        self.cls_head = nn.Linear(64, num_classes)

    def forward(self, force_x, image):
        force_feat = self.force_proj(force_x)

        img_feat = self.image_backbone(image)
        img_feat = self.image_pool(img_feat).flatten(1)
        img_feat = self.image_proj(img_feat)

        fused = self.fusion(torch.cat([force_feat, img_feat], dim=1))
        return {
            "wear_reg": self.reg_head(fused),
            "wear_cls": self.cls_head(fused),
        }
