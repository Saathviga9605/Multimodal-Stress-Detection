import numpy as np
import pandas as pd
from stressres.clean.face import FaceFrameTable
from stressres.types import WindowSpec

TARGET_AUS = [
    "AU01", "AU02", "AU04", "AU05", "AU06", "AU07", "AU09", "AU10",
    "AU12", "AU14", "AU15", "AU17", "AU20", "AU23", "AU25", "AU26", "AU28", "AU45"
]


def extract_face_features(frame_table: FaceFrameTable, spec: WindowSpec) -> dict[str, float | None]:
    """
    Extract facial Action Units, gaze, and pose features for one window.
    Per FEATURE_EXTRACTION_PROTOCOL.md Section 3.4.
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

    # 1. Action Units intensity, presence, and temporal derivatives
    for au in TARGET_AUS:
        r_col = f"{au}_r"
        c_col = f"{au}_c"

        if r_col in w_df.columns:
            vals = w_df[r_col].values.astype(np.float64)
            feats[f"{r_col}_mean"] = float(np.mean(vals))
            feats[f"{r_col}_std"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            
            # Temporal derivative (|delta|)
            dvals = np.abs(np.diff(vals))
            feats[f"{r_col}_diff_mean"] = float(np.mean(dvals)) if len(dvals) > 0 else 0.0

        if c_col in w_df.columns:
            p_vals = w_df[c_col].values.astype(np.float64)
            feats[f"{c_col}_presence_rate"] = float(np.mean(p_vals))

    # 2. Gaze direction vectors
    gaze_cols = [c for c in w_df.columns if "gaze" in c.lower()]
    for col in gaze_cols:
        g_vals = w_df[col].values.astype(np.float64)
        feats[f"{col}_mean"] = float(np.mean(g_vals))
        feats[f"{col}_std"] = float(np.std(g_vals, ddof=1)) if len(g_vals) > 1 else 0.0

    # 3. Head pose dynamics (pitch, yaw, roll)
    pose_cols = [c for c in w_df.columns if "pose" in c.lower()]
    for col in pose_cols:
        p_vals = w_df[col].values.astype(np.float64)
        feats[f"{col}_mean"] = float(np.mean(p_vals))
        feats[f"{col}_std"] = float(np.std(p_vals, ddof=1)) if len(p_vals) > 1 else 0.0
        
        # Velocity
        v_vals = np.abs(np.diff(p_vals))
        feats[f"{col}_velocity_mean"] = float(np.mean(v_vals)) if len(v_vals) > 0 else 0.0

    return feats
