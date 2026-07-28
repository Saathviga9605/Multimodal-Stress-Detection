import plotly.graph_objects as go
import numpy as np
import streamlit as st


def render_signal_viewer(clean_data: dict, subject_id: str):
    """
    V2 — Raw Signal & Peak Inspector
    Zoomable ECG / EDA / RESP trace viewer with detected event overlays.
    """
    st.subheader("V2 — Raw Signal & Processing Inspector")
    st.caption("Inspect filtered continuous signals, detected R-peaks, and SCR peaks.")

    modality = st.radio("Select Signal Channel", options=["ECG", "EDA", "RESP"], horizontal=True, key="v2_mod")

    if modality.lower() not in clean_data or clean_data[modality.lower()] is None:
        st.info(f"Clean {modality} signal data not loaded for subject {subject_id}.")
        return

    sig_npz = clean_data[modality.lower()]
    filtered = sig_npz.get("filtered", np.array([]))
    fs = float(sig_npz.get("fs", 700.0 if modality.lower() == "ecg" else 8.0))

    if len(filtered) == 0:
        st.warning(f"No signal data in {modality} npz file.")
        return

    time_axis = np.arange(len(filtered)) / fs

    fig = go.Figure()

    # Main signal trace
    fig.add_trace(
        go.Scatter(
            x=time_axis,
            y=filtered,
            mode="lines",
            name=f"Clean {modality}",
            line=dict(color="#2980b9" if modality == "ECG" else ("#27ae60" if modality == "EDA" else "#8e44ad"), width=1.5),
        )
    )

    # Peak overlays
    if modality == "ECG" and "r_peaks" in sig_npz:
        r_peaks = sig_npz["r_peaks"]
        if len(r_peaks) > 0:
            fig.add_trace(
                go.Scatter(
                    x=r_peaks / fs,
                    y=filtered[r_peaks],
                    mode="markers",
                    name="Detected R-Peaks",
                    marker=dict(color="#e74c3c", size=6, symbol="x"),
                )
            )

    elif modality == "EDA" and "scr_peaks" in sig_npz:
        scr_peaks = sig_npz["scr_peaks"]
        if len(scr_peaks) > 0:
            fig.add_trace(
                go.Scatter(
                    x=scr_peaks / fs,
                    y=filtered[scr_peaks],
                    mode="markers",
                    name="SCR Peak Events",
                    marker=dict(color="#e67e22", size=8, symbol="triangle-up"),
                )
            )

    fig.update_layout(
        title=f"{modality} Signal Inspection — Subject {subject_id}",
        xaxis_title="Time (seconds)",
        yaxis_title=f"{modality} Amplitude",
        height=450,
        margin=dict(l=20, r=20, t=50, b=50),
    )

    st.plotly_chart(fig, width="stretch")
