from pathlib import Path
import numpy as np
import pandas as pd
import cv2
from stressres.clean.face import FaceFrameTable
from stressres.types import Block, RawSession, Signal


def load_stressid_video_frames(
    subject_id: str,
    raw_root: Path,
    labels_df: pd.DataFrame | None = None,
) -> RawSession:
    """
    Loads MP4 video files for one StressID subject and generates FaceFrameTable per task.
    """
    video_dir = raw_root / "Videos"
    if not video_dir.exists():
        video_dir = raw_root

    signals: dict[str, Signal] = {}
    blocks: list[Block] = []
    source_files: list[Path] = []

    vid_files = [f for f in video_dir.glob(f"**/{subject_id}_*.mp4") if not f.name.startswith("._")]
    current_time = 0.0

    for vf in sorted(vid_files):
        fname = vf.stem
        parts = fname.split("_")
        if len(parts) < 2:
            continue
        task_name = parts[1]

        cap = cv2.VideoCapture(str(vf))
        if not cap.isOpened():
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 15.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / float(fps)
        cap.release()

        source_files.append(vf)
        t_start = current_time
        t_end = current_time + duration

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

    # Dummy continuous signal marker for video session
    signals["face"] = Signal(
        name="face",
        data=np.array([0.0]),
        fs=15.0,
        unit="fps",
        site="webcam",
    )

    return RawSession(
        dataset="stressid",
        subject_id=subject_id,
        signals=signals,
        blocks=blocks,
        source_files=source_files,
    )
