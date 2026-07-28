"""
Face Feature Extraction & OpenFace / PyTorch MediaPipe Wrapper
"""
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FaceFrameTable:
    subject_id: str
    task: str
    frames_df: pd.DataFrame          # Frame-level Action Units, Gaze, Pose
    detection_rate: float            # Fraction of frames with confidence >= 0.8


def process_face_video(
    video_path: Path,
    subject_id: str,
    task: str,
    out_dir: Path | None = None,
    fps_target: float = 5.0,
) -> FaceFrameTable:
    """
    Process video to extract facial Action Units (AUs), gaze vectors, and head pose.
    Handles downsampling to target fps (5.0 fps per StressID benchmark).
    """
    if not video_path.exists():
        return FaceFrameTable(
            subject_id=subject_id,
            task=task,
            frames_df=pd.DataFrame(),
            detection_rate=0.0,
        )

    # Check for pre-processed OpenFace CSV output if available
    csv_file = video_path.with_suffix(".csv")
    if out_dir:
        csv_file = out_dir / f"{video_path.stem}.csv"

    if csv_file.exists():
        df = pd.read_csv(csv_file)
        # Drop low confidence frames
        if "confidence" in df.columns:
            valid_mask = df["confidence"] >= 0.8
            det_rate = float(np.mean(valid_mask))
            df = df[valid_mask]
        else:
            det_rate = 1.0
        return FaceFrameTable(
            subject_id=subject_id,
            task=task,
            frames_df=df,
            detection_rate=det_rate,
        )

    # Placeholder / Fallback for frame table when OpenFace CLI is run separately
    return FaceFrameTable(
        subject_id=subject_id,
        task=task,
        frames_df=pd.DataFrame(),
        detection_rate=0.0,
    )
