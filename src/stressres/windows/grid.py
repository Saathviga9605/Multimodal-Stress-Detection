import numpy as np
from stressres.admissibility import admissible_features
from stressres.types import Block, RawSession, WindowSpec


def build_window_specs_for_session(
    session: RawSession,
    modality: str = "ecg",
    window_s: float = 60.0,
    stride_s: float | None = 5.0,
    trim_onset_s: float = 30.0,
) -> list[WindowSpec]:
    """
    Constructs Stage 2 WindowSpec objects for a RawSession.
    """
    specs: list[WindowSpec] = []
    dataset = session.dataset.lower()
    subject_id = session.subject_id

    for block in session.blocks:
        effective_trim = 0.0 if dataset == "stressid" else trim_onset_s
        t_block_start = block.t_start + effective_trim
        t_block_end = block.t_end

        if t_block_end - t_block_start < window_s:
            continue

        if stride_s is None or dataset == "stressid" and block.name in [
            "Counting1", "Counting2", "Counting3", "Math", "Reading", "Speaking", "Stroop"
        ]:
            # Exactly 1 window per task (or single non-overlapping window)
            window_starts = [block.t_start]
        else:
            window_starts = np.arange(t_block_start, t_block_end - window_s + 1e-5, stride_s)

        for i, w_start in enumerate(window_starts):
            w_end = w_start + window_s
            if w_end > block.t_end + 1e-4:
                continue

            window_id = f"{dataset}_{subject_id}_{block.name}_{modality}_w{i:04d}"
            is_baseline = (
                (dataset == "wesad" and block.name == "baseline") or
                (dataset == "stressid" and block.name in ("Breathing", "Relax"))
            )

            # Compute admissible features
            adm = admissible_features(
                modality=modality,
                duration_s=window_s,
                task=block.name,
                dataset=dataset,
            )

            spec = WindowSpec(
                dataset=dataset,
                subject_id=subject_id,
                task=block.name,
                modality=modality,
                window_id=window_id,
                t_start=float(w_start),
                t_end=float(w_end),
                label_binary=block.label_binary if block.label_binary is not None else 0,
                label_source=block.label_source,
                ratings=block.ratings,
                is_baseline=is_baseline,
                admissible=adm,
            )
            specs.append(spec)

    return specs
