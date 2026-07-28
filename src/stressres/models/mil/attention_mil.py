import torch
import torch.nn as nn
import torch.nn.functional as F


class AttentionMILPool(nn.Module):
    """
    Attention-based Multiple Instance Learning (Ilse et al. 2018).
    Treats task recordings as bags and 10s/60s windows as instances.
    Extracts attention weights per window to discover peak stress moments.
    """

    def __init__(self, in_features: int, hidden_dim: int = 64, gated: bool = True):
        super().__init__()
        self.gated = gated
        self.feature_extractor = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
        )

        if gated:
            self.attention_V = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.Tanh())
            self.attention_U = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.Sigmoid())
            self.attention_weights = nn.Linear(hidden_dim, 1)
        else:
            self.attention = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim),
                nn.Tanh(),
                nn.Linear(hidden_dim, 1),
            )

        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 2),
        )

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """
        x: (batch_size, n_instances, in_features)
        Returns: logits (batch_size, 2), attention_weights (batch_size, n_instances)
        """
        h = self.feature_extractor(x)  # (B, N, H)

        if self.gated:
            a_v = self.attention_V(h)
            a_u = self.attention_U(h)
            a = self.attention_weights(a_v * a_u)  # (B, N, 1)
        else:
            a = self.attention(h)  # (B, N, 1)

        a_weights = F.softmax(a, dim=1)  # (B, N, 1)
        bag_representation = torch.sum(a_weights * h, dim=1)  # (B, H)

        logits = self.classifier(bag_representation)  # (B, 2)
        return logits, a_weights.squeeze(-1)
