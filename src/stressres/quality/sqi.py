"""
Signal Quality Index (SQI) Functions per Modality
"""
from dataclasses import dataclass
import numpy as np
from stressres.clean.ecg import CleanECG
from stressres.clean.eda import CleanEDA
from stressres.clean.resp import CleanRESP


@dataclass(frozen=True)
class QualityResult:
    sqi: float                       # [0.0, 1.0]
    reason: str                      # Empty string if sqi == 1.0


def compute_ecg_sqi(clean: CleanECG) -> QualityResult:
    """ECG SQI score in [0.0, 1.0]."""
    if clean.n_valid_rr < 20:
        return QualityResult(0.0, "insufficient_valid_rr_count")
    if clean.pct_ectopic > 0.05:
        return QualityResult(0.0, "high_ectopic_rate")

    # Check heart rate bounds (30 - 200 bpm)
    hrs = 60.0 / clean.rr_intervals
    valid_hr_pct = np.mean((hrs >= 30.0) & (hrs <= 200.0))
    if valid_hr_pct < 0.8:
        return QualityResult(0.0, "unphysiological_heart_rate")

    sqi = float(max(0.0, min(1.0, (1.0 - clean.pct_ectopic) * valid_hr_pct)))
    return QualityResult(sqi, "" if sqi > 0.8 else "moderate_noise")


def compute_eda_sqi(clean: CleanEDA) -> QualityResult:
    """EDA SQI score in [0.0, 1.0]."""
    sig = clean.filtered
    if len(sig) == 0:
        return QualityResult(0.0, "empty_eda_signal")

    # Flat line / detachment detection
    if np.std(sig) < 1e-4 or np.max(sig) < 0.01:
        return QualityResult(0.0, "flatline_or_electrode_detachment")

    # Physiological range check (0.01 to 100 uS)
    in_range_pct = float(np.mean((sig >= 0.01) & (sig <= 100.0)))
    if in_range_pct < 0.8:
        return QualityResult(0.0, "out_of_range_values")

    return QualityResult(in_range_pct, "" if in_range_pct > 0.9 else "range_artifacts")


def compute_resp_sqi(clean: CleanRESP) -> QualityResult:
    """RESP SQI score in [0.0, 1.0]."""
    rate = clean.resp_rate
    if rate < 4.0 or rate > 40.0:
        return QualityResult(0.0, "unphysiological_breath_rate")
    return QualityResult(1.0, "")
