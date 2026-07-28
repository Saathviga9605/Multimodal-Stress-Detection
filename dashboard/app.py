from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

from dashboard.components.timeline import render_protocol_timeline
from dashboard.components.signal_viewer import render_signal_viewer
from dashboard.components.effect_size import render_effect_size_heatmap
from dashboard.components.time_course import render_within_task_time_course
from dashboard.components.label_dist import render_label_distribution
from dashboard.components.sqi_monitor import render_sqi_monitor

st.set_page_config(
    page_title="Multimodal Stress Research Dashboard",
    page_icon="🧠",
    layout="wide",
)

repo_root = Path(__file__).resolve().parent.parent


@st.cache_data
def load_parquet_data(path_str: str) -> pd.DataFrame:
    p = repo_root / path_str
    if p.exists():
        return pd.read_parquet(p)
    return pd.DataFrame()


@st.cache_data
def load_clean_signal_npz(dataset: str, subject: str) -> dict:
    clean_dir = repo_root / "data" / "processed" / "clean" / dataset / subject
    res = {}
    for mod in ["ecg", "eda", "resp"]:
        f_path = clean_dir / f"{mod}.npz"
        if f_path.exists():
            res[mod] = dict(np.load(f_path, allow_pickle=True))
        else:
            res[mod] = None
    return res


def main():
    st.title("🧠 Multimodal Stress Detection — Research & Diagnostic Dashboard")
    st.markdown(
        "A diagnostic instrument for verifying label validity, signal quality, and response effect sizes across **WESAD** and **StressID**."
    )

    st.sidebar.header("Dataset & Input Selector")
    dataset = st.sidebar.selectbox("Dataset", options=["wesad", "stressid"], index=0)
    modality = st.sidebar.selectbox("Modality", options=["ecg", "eda", "resp"], index=0)

    index_path = f"data/processed/index/{dataset}_{modality}_index.parquet"
    feature_path = f"data/processed/features/{dataset}_{modality}_features_anchored.parquet"

    df_index = load_parquet_data(index_path)
    df_features = load_parquet_data(feature_path)

    if df_features.empty:
        # Fallback to un-anchored feature file
        fallback_path = f"data/processed/features/{dataset}_{modality}_features.parquet"
        df_features = load_parquet_data(fallback_path)

    st.sidebar.markdown("---")
    st.sidebar.metric("Loaded Windows", len(df_features) if not df_features.empty else 0)
    st.sidebar.metric("Subjects Count", df_features["subject_id"].nunique() if not df_features.empty else 0)

    tabs = st.tabs([
        "V1: Protocol Timeline",
        "V2: Signal Inspector",
        "V3: Effect Size (Cohen's d)",
        "V4: Task Time-Course",
        "V5: Label Distribution",
        "V6: Quality Monitor",
    ])

    with tabs[0]:
        render_protocol_timeline(df_index)

    with tabs[1]:
        subjects = sorted(df_features["subject_id"].unique()) if not df_features.empty else ["S2"]
        selected_sub = st.selectbox("Select Subject for Signal Viewing", options=subjects, key="app_subj")
        clean_data = load_clean_signal_npz(dataset, selected_sub)
        render_signal_viewer(clean_data, selected_sub)

    with tabs[2]:
        render_effect_size_heatmap(df_features)

    with tabs[3]:
        render_within_task_time_course(df_features)

    with tabs[4]:
        render_label_distribution(df_features)

    with tabs[5]:
        render_sqi_monitor(df_features)


if __name__ == "__main__":
    main()
