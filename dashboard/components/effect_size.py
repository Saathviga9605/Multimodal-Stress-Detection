import numpy as np
import plotly.express as px
import pandas as pd
import streamlit as st
from dashboard.utils.metrics import compute_subject_effect_sizes


def render_effect_size_heatmap(df_features: pd.DataFrame):
    """
    V3 — Per-Subject Effect Size (Cohen's d Heatmap) View
    Directly measures label validity per subject (d > 0.8 target for physiological response).
    """
    st.subheader("V3 — Per-Subject Effect Size (Cohen's d Heatmap)")
    st.caption("Measures response magnitude between calm and stress windows per subject.")

    if df_features.empty:
        st.warning("No feature dataset loaded.")
        return

    meta_cols = {
        "dataset", "subject_id", "task", "window_id", "t_start", "t_end",
        "modality", "label_binary", "label_source", "is_baseline",
        "extractor_version", "config_hash", "quality", "quality_reason"
    }
    num_cols = df_features.select_dtypes(include=[np.number]).columns
    feature_cols = [c for c in num_cols if c not in meta_cols and c.endswith("_raw")]

    if not feature_cols:
        feature_cols = [c for c in num_cols if c not in meta_cols][:15]

    df_d = compute_subject_effect_sizes(df_features, feature_cols)
    df_d = df_d.set_index("subject_id")

    fig = px.imshow(
        df_d.T,
        labels=dict(x="Subject ID", y="Feature Metric", color="Cohen's d"),
        x=df_d.index,
        y=df_d.columns,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Subject x Feature Response Magnitude (Cohen's d)",
    )

    fig.update_layout(height=500, margin=dict(l=20, r=20, t=50, b=50))
    st.plotly_chart(fig, width="stretch")

    # Highlight low responders (d < 0.2 across all features)
    mean_d = df_d.abs().mean(axis=1)
    low_responders = mean_d[mean_d < 0.2].index.tolist()
    if low_responders:
        st.warning(f"⚠️ Potential Low-Responders / Unresponsive Subjects (mean |d| < 0.2): {', '.join(low_responders)}")
    else:
        st.success("✅ All subjects demonstrate measurable physiological response variations between conditions.")
