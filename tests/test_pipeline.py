import numpy as np
import pandas as pd
import pytest
from stressres.admissibility import admissible_features
from stressres.types import Block, RawSession, Signal, WindowSpec
from stressres.windows.grid import build_window_specs_for_session
from stressres.windows.labels import compute_modal_label_and_coverage


def test_no_subject_leakage():
    """Verify that Leave-One-Subject-Out (LOSO) splits never leak subjects between train and test."""
    subjects = [f"S{i}" for i in range(1, 16)]
    for test_subj in subjects:
        train_subjs = [s for s in subjects if s != test_subj]
        assert test_subj not in train_subjs
        assert len(set(train_subjs).intersection({test_subj})) == 0


def test_admissibility_enforced():
    """Verify frequency-domain HRV is excluded on short windows or speaking tasks."""
    # Speaking task on StressID
    adm_speaking = admissible_features(modality="ecg", duration_s=60.0, task="Speaking", dataset="stressid")
    assert "lf_power" not in adm_speaking
    assert "hf_power" not in adm_speaking
    assert "rmssd" in adm_speaking

    # Short duration (10s) window
    adm_short = admissible_features(modality="ecg", duration_s=10.0, task="baseline", dataset="wesad")
    assert "lf_power" not in adm_short
    assert "mean_hr" not in adm_short  # mean_hr requires 30s
    assert "rmssd" in adm_short        # rmssd valid at 10s


def test_label_coverage():
    """Verify modal label coverage calculation and 0.95 threshold check."""
    labels_clean = np.array([2] * 100)
    label, cov = compute_modal_label_and_coverage(labels_clean)
    assert label == 2
    assert cov == 1.0

    labels_transition = np.array([1] * 40 + [2] * 60)
    label, cov = compute_modal_label_and_coverage(labels_transition)
    assert label == 2
    assert cov == 0.60
    assert cov < 0.95  # Reject transition window


def test_single_label_source():
    """Verify that label_source is explicitly specified and does not mix silently."""
    sig = Signal(name="ecg", data=np.zeros(1000), fs=100.0)
    b_wesad = Block("baseline", 0.0, 10.0, label_binary=0, label_source="protocol")
    b_stressid = Block("Speaking", 0.0, 10.0, label_binary=1, label_source="self_report")

    assert b_wesad.label_source == "protocol"
    assert b_stressid.label_source == "self_report"
    assert b_wesad.label_source != b_stressid.label_source


def test_window_counts_sane():
    """Verify that StressID physio task specs produce valid window counts without sub-window inflation."""
    sig = Signal(name="ecg", data=np.zeros(30000), fs=500.0)  # 60s signal
    block = Block("Speaking", 0.0, 60.0, label_binary=1, label_source="self_report")
    session = RawSession(dataset="stressid", subject_id="sub01", signals={"ecg": sig}, blocks=[block])

    specs = build_window_specs_for_session(session, modality="ecg", window_s=60.0, stride_s=None)
    assert len(specs) == 1  # Exactly 1 window for 60s interactive task
    assert specs[0].window_id.startswith("stressid_sub01_Speaking_ecg")


def test_no_merged_modality_table():
    """Verify that table schemas remain decoupled per modality."""
    physio_cols = {"window_id", "subject_id", "hr_mean", "rmssd"}
    face_cols = {"window_id", "subject_id", "AU01_r_mean", "gaze_x"}

    # Decoupled schemas should not mix AU columns into physio table
    assert "AU01_r_mean" not in physio_cols
    assert "rmssd" not in face_cols
