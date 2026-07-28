import numpy as np
import pandas as pd
from stressres.clean.face import FaceFrameTable
from stressres.types import WindowSpec


def extract_face_features(frame_table: FaceFrameTable, spec: WindowSpec) -> dict[str, float | None]:
    """
    Extract facial Action Units, gaze, and pose features for one window.
    """
    df = frame_table.frames_df
    if df.empty or "timestamp" not in df.columns:
        return {}

    # Subset window frames
    mask = (df["timestamp"] >= spec.t_start) & (df["timestamp"] <= spec.t_end)
    w_df = df[mask]

    if w_df.empty:
        return {}

    feats = {}

    # Action Units columns (e.g. AU01_r, AU02_r, ...)
    au_cols = [c for c in w_df.columns if c.startswith("AU")]
    for col in au_cols:
        vals = w_df[col].values
        feats[f"{col}_mean"] = float(np.mean(vals))
        feats[f"{col}_std"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        # Temporal derivative
        dvals = np.abs(np.diff(vals))
        feats[f"{col}_diff_mean"] = float(np.mean(dvals)) if len(dvals) > 0 else 0.0

    return feats
