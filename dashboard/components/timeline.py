import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def render_protocol_timeline(df_index: pd.DataFrame):
    """
    V1 — Protocol Timeline View
    Renders horizontal timeline with condition/task blocks and binary labels overlaid.
    """
    st.subheader("V1 — Protocol Timeline Inspector")
    st.caption("Displays session tasks, window time bounds, and condition labels side-by-side.")

    if df_index.empty:
        st.warning("No window index data loaded.")
        return

    dataset = st.selectbox("Select Dataset", options=df_index["dataset"].unique(), key="v1_ds")
    sub_df = df_index[df_index["dataset"] == dataset]

    subjects = sorted(sub_df["subject_id"].unique())
    selected_subj = st.selectbox("Select Subject", options=subjects, key="v1_subj")

    subj_df = sub_df[sub_df["subject_id"] == selected_subj].sort_values("t_start")

    if subj_df.empty:
        st.info("No timeline records for selected subject.")
        return

    fig = go.Figure()

    # Color map for binary label
    colors = {0: "#2ecc71", 1: "#e74c3c"}
    labels_map = {0: "Non-Stress", 1: "Stress"}

    for _, row in subj_df.iterrows():
        fig.add_trace(
            go.Bar(
                x=[row["t_end"] - row["t_start"]],
                y=[row["task"]],
                base=row["t_start"],
                orientation="h",
                marker=dict(color=colors.get(row["label_binary"], "#3498db")),
                name=labels_map.get(row["label_binary"], "Unknown"),
                hoverinfo="text",
                hovertext=f"Task: {row['task']}<br>Start: {row['t_start']:.1f}s<br>End: {row['t_end']:.1f}s<br>Label: {labels_map.get(row['label_binary'])}",
                showlegend=False,
            )
        )

    fig.update_layout(
        title=f"Protocol Timeline for {dataset.upper()} Subject {selected_subj}",
        xaxis_title="Time (seconds)",
        yaxis_title="Task / Condition",
        barmode="stack",
        height=400,
        margin=dict(l=20, r=20, t=50, b=50),
    )

    st.plotly_chart(fig, width="stretch")
