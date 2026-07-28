import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st


def render_within_task_time_course(df_features: pd.DataFrame):
    """
    V4 — Within-Task Time Course
    Aligns stress recordings to task onset (t=0) and plots mean & IQR envelope across subjects.
    """
    st.subheader("V4 — Within-Task Response Dynamics & Time-Course")
    st.caption("Inspects whether physiological response ramps, sustains, or decays over task duration.")

    if df_features.empty:
        st.warning("No feature dataset loaded.")
        return

    meta_cols = {
        "dataset", "subject_id", "task", "window_id", "t_start", "t_end",
        "modality", "label_binary", "label_source", "is_baseline",
        "extractor_version", "config_hash", "quality", "quality_reason"
    }
    feature_cols = [c for c in df_features.columns if c not in meta_cols]
    selected_feat = st.selectbox("Select Feature Metric", options=feature_cols, key="v4_feat")

    tasks = df_features["task"].unique()
    selected_task = st.selectbox("Select Task / Condition", options=tasks, key="v4_task")

    t_df = df_features[df_features["task"] == selected_task].copy()
    if t_df.empty:
        st.info("No recordings for selected task.")
        return

    # Normalize relative start time
    t_df["rel_t"] = t_df.groupby("subject_id")["t_start"].transform(lambda x: x - x.min())

    grouped = t_df.groupby("rel_t")[selected_feat].agg(
        mean="mean",
        std="std",
        q25=lambda x: np.percentile(x.dropna(), 25) if len(x.dropna()) > 0 else np.nan,
        q75=lambda x: np.percentile(x.dropna(), 75) if len(x.dropna()) > 0 else np.nan,
    ).reset_index()

    fig = go.Figure()

    # Mean curve
    fig.add_trace(
        go.Scatter(
            x=grouped["rel_t"],
            y=grouped["mean"],
            mode="lines+markers",
            name="Mean Trajectory",
            line=dict(color="#e74c3c", width=2),
        )
    )

    # IQR Envelope
    fig.add_trace(
        go.Scatter(
            x=grouped["rel_t"],
            y=grouped["q75"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=grouped["rel_t"],
            y=grouped["q25"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(231, 76, 60, 0.2)",
            name="IQR (25th-75th percentile)",
        )
    )

    fig.update_layout(
        title=f"Time-Course Trajectory: {selected_feat} during '{selected_task}' Task",
        xaxis_title="Time from Task Onset (seconds)",
        yaxis_title=selected_feat,
        height=450,
        margin=dict(l=20, r=20, t=50, b=50),
    )

    st.plotly_chart(fig, width="stretch")
