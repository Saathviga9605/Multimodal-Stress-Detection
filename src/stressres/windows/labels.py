from typing import Tuple
import numpy as np


def compute_modal_label_and_coverage(labels_in_window: np.ndarray) -> Tuple[int, float]:
    """
    Computes modal label code and its coverage fraction over the window.
    """
    if len(labels_in_window) == 0:
        return 0, 0.0

    vals, counts = np.unique(labels_in_window, return_counts=True)
    max_idx = np.argmax(counts)
    modal_label = int(vals[max_idx])
    coverage = float(counts[max_idx]) / float(len(labels_in_window))
    return modal_label, coverage
