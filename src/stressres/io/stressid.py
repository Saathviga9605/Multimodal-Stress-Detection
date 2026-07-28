import csv
from pathlib import Path
import numpy as np
import pandas as pd
from stressres.types import Block, RawSession, Signal

STRESSID_TASKS = {
    "Breathing",
    "Counting1",
    "Video1",
    "Video2",
    "Counting2",
    "Stroop",
    "Speaking",
    "Math",
    "Reading",
    "Counting3",
    "Relax",
}


def load_stressid(
    subject_id: str,
    raw_root: Path,
    labels_df: pd.DataFrame | None = None,
    self_assessments_path: Path | None = None,
) -> RawSession:
    """
    Load all available physiological recordings and metadata for one StressID subject.
    
    Reads ECG, EDA, RESP signals (500 Hz native) and extracts per-task Block objects.
    """
    physio_dir = raw_root / "Physiological"
    if not physio_dir.exists():
        physio_dir = raw_root

    signals: dict[str, Signal] = {}
    blocks: list[Block] = []
    source_files: list[Path] = []

    # Find all .txt or .csv files for this subject in Physiological directory & subdirectories
    task_files = list(physio_dir.glob(f"**/{subject_id}_*.txt")) + list(physio_dir.glob(f"**/{subject_id}_*.csv"))

    # Parse self-assessment ratings if path given
    ratings_map = _load_self_assessments(self_assessments_path) if self_assessments_path else {}
    labels_map = _load_labels_map(labels_df) if labels_df is not None else {}

    ecg_concat, eda_concat, resp_concat = [], [], []
    current_time = 0.0

    for tf in sorted(task_files):
        # Filename format: {subject_id}_{task}.txt or .csv
        fname = tf.stem
        parts = fname.split("_")
        if len(parts) < 2:
            continue
        task_name = parts[1]

        if task_name not in STRESSID_TASKS:
            continue

        try:
            df = pd.read_csv(tf)
        except Exception:
            continue

        source_files.append(tf)
        n_samples = len(df)
        duration = n_samples / 500.0
        t_start = current_time
        t_end = current_time + duration

        # Extract column signals (ECG, EDA, RESP/RR)
        cols = {c.lower(): c for c in df.columns}
        if "ecg" in cols:
            ecg_concat.append(df[cols["ecg"]].values.astype(np.float64))
        if "eda" in cols:
            eda_concat.append(df[cols["eda"]].values.astype(np.float64))
        
        resp_col = cols.get("resp", cols.get("respiration", cols.get("rr")))
        if resp_col:
            resp_concat.append(df[resp_col].values.astype(np.float64))

        # Get task ratings and binary label
        key = f"{subject_id}_{task_name}"
        ratings = ratings_map.get(key, {})
        
        # Binary label priority: labels.csv > self_assessments (stress >= 5) > 0
        if key in labels_map:
            binary_label = labels_map[key]
        elif "stress" in ratings:
            binary_label = 1 if ratings["stress"] >= 5.0 else 0
        else:
            binary_label = 0

        blocks.append(
            Block(
                name=task_name,
                t_start=t_start,
                t_end=t_end,
                label_binary=binary_label,
                label_source="self_report",
                ratings=ratings,
            )
        )

        current_time = t_end

    # Concatenate continuous signals across session tasks
    if ecg_concat:
        signals["ecg"] = Signal(
            name="ecg",
            data=np.concatenate(ecg_concat),
            fs=500.0,
            unit="mV",
            site="ribs",
        )
    if eda_concat:
        signals["eda"] = Signal(
            name="eda",
            data=np.concatenate(eda_concat),
            fs=500.0,
            unit="uS",
            site="palm",
        )
    if resp_concat:
        signals["resp"] = Signal(
            name="resp",
            data=np.concatenate(resp_concat),
            fs=500.0,
            unit="mV",
            site="chest",
        )

    return RawSession(
        dataset="stressid",
        subject_id=subject_id,
        signals=signals,
        blocks=blocks,
        source_files=source_files,
    )


def _load_labels_map(labels_df: pd.DataFrame) -> dict[str, int]:
    """Build key -> binary label map from labels.csv."""
    res = {}
    if labels_df is None or labels_df.empty:
        return res
    for _, row in labels_df.iterrows():
        key = str(row.iloc[0]).strip()
        val = int(row.iloc[1])
        res[key] = val
    return res


def _load_self_assessments(csv_path: Path) -> dict[str, dict[str, float]]:
    """Parse self_assessments.csv (Semicolon-separated) into ratings map."""
    res = {}
    if not csv_path or not csv_path.exists():
        return res

    try:
        df = pd.read_csv(csv_path, sep=";")
        if "Tasks" not in df.columns:
            return res

        subject_ids = [c for c in df.columns if c != "Tasks"]

        for _, row in df.iterrows():
            task_metric = str(row["Tasks"]).strip()
            if "_" not in task_metric:
                continue
            parts = task_metric.split("_")
            task_name, metric = parts[0], parts[1].lower()

            for subj in subject_ids:
                val_str = str(row[subj]).strip()
                if not val_str or val_str.lower() == "nan":
                    continue
                try:
                    val = float(val_str)
                    key = f"{subj}_{task_name}"
                    if key not in res:
                        res[key] = {}
                    res[key][metric] = val
                except ValueError:
                    continue
    except Exception:
        pass

    return res
