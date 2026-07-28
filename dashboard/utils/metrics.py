import numpy as np
import pandas as pd


def compute_cohens_d(x1: np.ndarray, x2: np.ndarray) -> float:
    """
    Computes Cohen's d effect size between group 1 (stress) and group 2 (calm/baseline).
    Positive d indicates feature increase during stress.
    """
    x1_arr = pd.to_numeric(pd.Series(x1), errors="coerce").values
    x2_arr = pd.to_numeric(pd.Series(x2), errors="coerce").values
    
    x1_clean = x1_arr[~np.isnan(x1_arr)]
    x2_clean = x2_arr[~np.isnan(x2_arr)]

    n1, n2 = len(x1_clean), len(x2_clean)
    if n1 < 2 or n2 < 2:
        return 0.0

    m1, m2 = float(np.mean(x1_clean)), float(np.mean(x2_clean))
    v1, v2 = float(np.var(x1_clean, ddof=1)), float(np.var(x2_clean, ddof=1))

    s_pooled = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    if s_pooled < 1e-8:
        return 0.0

    return (m1 - m2) / s_pooled


def compute_subject_effect_sizes(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """
    Computes Subject x Feature Cohen's d effect size matrix.
    """
    subjects = df["subject_id"].unique()
    matrix = []

    for s in sorted(subjects):
        s_df = df[df["subject_id"] == s]
        stress_df = s_df[s_df["label_binary"] == 1]
        calm_df = s_df[s_df["is_baseline"] == True]

        if calm_df.empty:
            calm_df = s_df[s_df["label_binary"] == 0]

        row = {"subject_id": s}
        for col in feature_cols:
            if col in s_df.columns:
                d_val = compute_cohens_d(
                    stress_df[col].values,
                    calm_df[col].values,
                )
                row[col] = d_val
            else:
                row[col] = np.nan
        matrix.append(row)

    return pd.DataFrame(matrix)
