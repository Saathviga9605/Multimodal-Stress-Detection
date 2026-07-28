import plotly.express as px
import pandas as pd
import streamlit as st


def render_label_distribution(df_features: pd.DataFrame):
    """
    V5 — Label Distribution & Rating Spectrum View
    Histogram of class balance and raw rating distributions.
    """
    st.subheader("V5 — Label Distribution & Target Spectrum")
    st.caption("Inspect class balance and rating distribution per dataset.")

    if df_features.empty:
        st.warning("No feature dataset loaded.")
        return

    col1, col2 = st.columns(2)

    with col1:
        # Binary class balance
        class_counts = df_features["label_binary"].value_counts().reset_index()
        class_counts.columns = ["label_binary", "count"]
        class_counts["Label"] = class_counts["label_binary"].map({0: "Non-Stress (0)", 1: "Stress (1)"})

        fig_pie = px.pie(
            class_counts,
            values="count",
            names="Label",
            title="Binary Class Balance",
            color_discrete_sequence=["#2ecc71", "#e74c3c"],
        )
        st.plotly_chart(fig_pie, width="stretch")

    with col2:
        # Per-task window distribution
        task_counts = df_features["task"].value_counts().reset_index()
        task_counts.columns = ["task", "count"]

        fig_bar = px.bar(
            task_counts,
            x="task",
            y="count",
            title="Window Count per Task / Condition",
            color="count",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_bar, width="stretch")
