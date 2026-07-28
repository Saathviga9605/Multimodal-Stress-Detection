from dataclasses import dataclass, field
import numpy as np
import pandas as pd


@dataclass
class BaselineProfile:
    subject_id: str
    modality: str
    valid: bool
    n_windows: int
    medians: dict[str, float] = field(default_factory=dict)
    mads: dict[str, float] = field(default_factory=dict)
    reason: str = ""


def build_baseline_profile(
    df: pd.DataFrame,
    subject_id: str,
    modality: str,
    feature_cols: list[str],
    min_windows: int = 3,
    min_quality: float = 0.5,
) -> BaselineProfile:
    """
    Computes robust median and MAD statistics over calm baseline windows for one subject.
    """
    # Filter for subject's calm baseline windows with quality > min_quality
    cond = (
        (df["subject_id"] == subject_id) &
        (df["is_baseline"] == True) &
        (df["quality"] >= min_quality)
    )
    base_df = df[cond]

    if len(base_df) < min_windows:
        return BaselineProfile(
            subject_id=subject_id,
            modality=modality,
            valid=False,
            n_windows=len(base_df),
            reason=f"insufficient_baseline_windows_{len(base_df)}<{min_windows}",
        )

    medians = {}
    mads = {}

    for col in feature_cols:
        if col in base_df.columns:
            vals = base_df[col].dropna().values
            if len(vals) > 0:
                med = float(np.median(vals))
                mad = float(np.median(np.abs(vals - med)))
                medians[col] = med
                mads[col] = mad

    return BaselineProfile(
        subject_id=subject_id,
        modality=modality,
        valid=True,
        n_windows=len(base_df),
        medians=medians,
        mads=mads,
    )


def anchor_features(
    df: pd.DataFrame,
    profile: BaselineProfile,
    feature_cols: list[str],
) -> pd.DataFrame:
    """
    Anchors features relative to baseline profile median and MAD.
    Emits both raw and anchored features (_raw and _anch) in output.
    """
    out_df = df.copy()

    for col in feature_cols:
        if col not in out_df.columns:
            continue

        raw_col_name = f"{col}_raw" if not col.endswith("_raw") else col
        anch_col_name = f"{col.replace('_raw', '')}_anch"

        # Preserve raw column
        out_df[raw_col_name] = out_df[col]

        if profile.valid and col in profile.medians and col in profile.mads:
            med = profile.medians[col]
            mad = profile.mads[col]
            out_df[anch_col_name] = (out_df[col] - med) / (1.4826 * mad + 1e-8)
        else:
            out_df[anch_col_name] = np.nan

    return out_df
