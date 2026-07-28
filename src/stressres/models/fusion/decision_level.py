import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


class LateDecisionFusion:
    """
    Decoupled Late Decision-Level Fusion.
    Combines posterior probability outputs from independent modality classifiers
    using average rule, sum rule, or weighted product rule without dropping subjects.
    """

    def __init__(self, rule: str = "average"):
        self.rule = rule

    def fuse_probabilities(self, prob_dict: dict[str, np.ndarray], weights: dict[str, float] | None = None) -> np.ndarray:
        """
        Combines modality probability arrays.
        prob_dict: {'ecg': probs, 'eda': probs, ...}
        """
        modalities = list(prob_dict.keys())
        if not modalities:
            raise ValueError("No modality probabilities provided for fusion.")

        if weights is None:
            weights = {m: 1.0 / len(modalities) for m in modalities}

        n_samples = len(prob_dict[modalities[0]])
        fused_probs = np.zeros((n_samples, 2))

        if self.rule == "average" or self.rule == "sum":
            total_weight = sum(weights.values())
            for m in modalities:
                fused_probs += prob_dict[m] * (weights[m] / total_weight)

        elif self.rule == "product":
            fused_probs = np.ones((n_samples, 2))
            for m in modalities:
                fused_probs *= (prob_dict[m] ** weights[m])
            # Re-normalize
            fused_probs = fused_probs / np.sum(fused_probs, axis=1, keepdims=True)

        return fused_probs

    def evaluate_fusion(
        self,
        prob_dict: dict[str, np.ndarray],
        y_true: np.ndarray,
        weights: dict[str, float] | None = None,
    ) -> dict:
        fused_probs = self.fuse_probabilities(prob_dict, weights)
        fused_preds = np.argmax(fused_probs, axis=1)

        acc = float(accuracy_score(y_true, fused_preds))
        f1 = float(f1_score(y_true, fused_preds))

        return {
            "accuracy": acc,
            "f1_score": f1,
            "fused_predictions": fused_preds,
            "fused_probabilities": fused_probs,
        }
