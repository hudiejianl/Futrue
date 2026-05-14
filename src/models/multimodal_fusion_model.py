import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small


class MultimodalFusionModel(nn.Module):
    def __init__(self, feature_input_dim: int, use_image: bool = True, num_classes: int = 4):
        super().__init__()
        self.use_image = use_image

        self.feature_proj = nn.Sequential(
            nn.Linear(feature_input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
        ) if feature_input_dim > 0 else None

        if use_image:
            backbone = mobilenet_v3_small(weights=None)
            self.image_backbone = backbone.features
            self.image_pool = nn.AdaptiveAvgPool2d((1, 1))
            self.image_proj = nn.Linear(576, 128)
            fusion_in = 64 + 128 if feature_input_dim > 0 else 128
        else:
            fusion_in = 64

        self.fusion = nn.Sequential(
            nn.Linear(fusion_in, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
        )
        self.reg_head = nn.Linear(64, 1)
        self.cls_head = nn.Linear(64, num_classes)

    def forward(self, features, image):
        feats = []
        if self.feature_proj is not None:
            feats.append(self.feature_proj(features))

        if self.use_image:
            img = self.image_backbone(image)
            img = self.image_pool(img).flatten(1)
            img = self.image_proj(img)
            feats.append(img)

        fused_input = feats[0] if len(feats) == 1 else torch.cat(feats, dim=1)
        fused = self.fusion(fused_input)
        return {
            "wear_reg": self.reg_head(fused),
            "wear_cls": self.cls_head(fused),
        }
