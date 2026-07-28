import plotly.express as px
import pandas as pd
import streamlit as st


def render_sqi_monitor(df_features: pd.DataFrame):
    """
    V6 — Signal Quality Index (SQI) Dashboard
    Quality score distribution and exclusion reason breakdown.
    """
    st.subheader("V6 — Signal Quality Index (SQI) Monitor")
    st.caption("Tracks quality scores and flags windows marked for exclusion.")

    if df_features.empty or "quality" not in df_features.columns:
        st.warning("No quality metadata in feature dataset.")
        return

    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            df_features,
            x="quality",
            nbins=20,
            title="Signal Quality Score Distribution (SQI)",
            color_discrete_sequence=["#34495e"],
        )
        st.plotly_chart(fig_hist, width="stretch")

    with col2:
        if "quality_reason" in df_features.columns:
            reasons = df_features["quality_reason"].value_counts().reset_index()
            reasons.columns = ["reason", "count"]
            reasons["reason"] = reasons["reason"].replace("", "Clean (Pass)")

            fig_reasons = px.bar(
                reasons,
                x="reason",
                y="count",
                title="Quality Rejection Reason Histogram",
                color="count",
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig_reasons, width="stretch")
