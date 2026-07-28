import pickle
from pathlib import Path
import numpy as np
from stressres.types import Block, RawSession, Signal


WESAD_VALID_LABELS = {
    1: ("baseline", 0),      # non-stress
    2: ("stress", 1),        # stress
    3: ("amusement", 0),     # non-stress
    4: ("meditation", 0),    # non-stress
}


def load_wesad(pkl_path: Path) -> RawSession:
    """
    Load one WESAD subject pickle (.pkl) file.
    
    Handles:
    - Python 2 latin1 encoding.
    - Resampling/aligning signals to native sample times.
    - Run-length encoding of label array to form Block list.
    """
    if not pkl_path.exists():
        raise FileNotFoundError(f"WESAD file not found: {pkl_path}")

    with open(pkl_path, "rb") as f:
        data = pickle.load(f, encoding="latin1")

    subject_id = data["subject"]
    raw_signals = data["signal"]
    raw_labels = np.asarray(data["label"]).flatten()

    signals: dict[str, Signal] = {}

    # Load Chest Signals (all native 700 Hz)
    chest_dict = raw_signals.get("chest", {})
    if "ECG" in chest_dict:
        signals["ecg"] = Signal(
            name="ecg",
            data=chest_dict["ECG"].flatten().astype(np.float64),
            fs=700.0,
            unit="mV",
            site="chest",
        )
    if "EDA" in chest_dict:
        signals["eda"] = Signal(
            name="eda",
            data=chest_dict["EDA"].flatten().astype(np.float64),
            fs=700.0,
            unit="uS",
            site="abdomen",
        )
    if "Resp" in chest_dict:
        signals["resp"] = Signal(
            name="resp",
            data=chest_dict["Resp"].flatten().astype(np.float64),
            fs=700.0,
            unit="mV",
            site="chest",
        )

    # Load Wrist Signals
    wrist_dict = raw_signals.get("wrist", {})
    if "BVP" in wrist_dict:
        signals["bvp_wrist"] = Signal(
            name="bvp_wrist",
            data=wrist_dict["BVP"].flatten().astype(np.float64),
            fs=64.0,
            unit="uW",
            site="wrist",
        )
    if "EDA" in wrist_dict:
        signals["eda_wrist"] = Signal(
            name="eda_wrist",
            data=wrist_dict["EDA"].flatten().astype(np.float64),
            fs=4.0,
            unit="uS",
            site="wrist",
        )

    # Convert continuous label array to Block spans via RLE
    blocks = _extract_wesad_blocks(raw_labels, fs=700.0)

    return RawSession(
        dataset="wesad",
        subject_id=str(subject_id),
        signals=signals,
        blocks=blocks,
        source_files=[pkl_path],
    )


def _extract_wesad_blocks(labels: np.ndarray, fs: float = 700.0) -> list[Block]:
    """Run-length encode 700Hz label array into list of Block objects."""
    blocks: list[Block] = []
    if len(labels) == 0:
        return blocks

    # Find transition indices
    changes = np.where(labels[:-1] != labels[1:])[0] + 1
    split_indices = np.concatenate(([0], changes, [len(labels)]))

    for start_idx, end_idx in zip(split_indices[:-1], split_indices[1:]):
        code = int(labels[start_idx])
        if code not in WESAD_VALID_LABELS:
            continue  # Drop 0 (transient), 5, 6, 7

        condition_name, binary_label = WESAD_VALID_LABELS[code]
        t_start = float(start_idx) / fs
        t_end = float(end_idx) / fs
        duration = t_end - t_start

        # Retain blocks with reasonable duration (e.g. >= 30s)
        if duration >= 30.0:
            blocks.append(
                Block(
                    name=condition_name,
                    t_start=t_start,
                    t_end=t_end,
                    label_binary=binary_label,
                    label_source="protocol",
                    ratings={},
                )
            )

    return blocks
