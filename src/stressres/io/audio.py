from pathlib import Path
import numpy as np
import pandas as pd
import soundfile as sf
from stressres.clean.voice import CleanVoice
from stressres.types import Block, RawSession, Signal


def load_stressid_audio(
    subject_id: str,
    raw_root: Path,
    labels_df: pd.DataFrame | None = None,
) -> RawSession:
    """
    Load all available WAV audio files for one StressID subject.
    """
    audio_dir = raw_root / "Audio"
    if not audio_dir.exists():
        audio_dir = raw_root

    signals: dict[str, Signal] = {}
    blocks: list[Block] = []
    source_files: list[Path] = []

    audio_files = [f for f in audio_dir.glob(f"**/{subject_id}_*.wav") if not f.name.startswith("._")]
    audio_concat = []
    current_time = 0.0

    for af in sorted(audio_files):
        fname = af.stem
        parts = fname.split("_")
        if len(parts) < 2:
            continue
        task_name = parts[1]

        try:
            data, fs = sf.read(af)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
        except Exception:
            continue

        source_files.append(af)
        n_samples = len(data)
        duration = n_samples / float(fs)
        t_start = current_time
        t_end = current_time + duration

        audio_concat.append(data)

        # Label lookup
        binary_label = 0
        if labels_df is not None and not labels_df.empty:
            key = f"{subject_id}_{task_name}"
            matches = labels_df[labels_df.iloc[:, 0].astype(str) == key]
            if not matches.empty:
                binary_label = int(matches.iloc[0, 1])

        blocks.append(
            Block(
                name=task_name,
                t_start=t_start,
                t_end=t_end,
                label_binary=binary_label,
                label_source="protocol",
            )
        )
        current_time = t_end

    if audio_concat:
        signals["voice"] = Signal(
            name="voice",
            data=np.concatenate(audio_concat),
            fs=16000.0,
            unit="amplitude",
            site="microphone",
        )

    return RawSession(
        dataset="stressid",
        subject_id=subject_id,
        signals=signals,
        blocks=blocks,
        source_files=source_files,
    )
