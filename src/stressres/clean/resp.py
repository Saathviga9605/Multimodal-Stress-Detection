from dataclasses import dataclass
import neurokit2 as nk
import numpy as np
from scipy.signal import butter, filtfilt
from stressres.types import Signal


@dataclass(frozen=True)
class CleanRESP:
    filtered: np.ndarray             # 1-D clean respiration signal
    peaks: np.ndarray                # Inhalation peaks indices
    troughs: np.ndarray              # Exhalation troughs indices
    resp_rate: float                 # Estimated mean breath rate (breaths/min)


def clean_resp(sig: Signal) -> CleanRESP:
    """
    Cleans respiration signal:
    1. Bandpass filter 0.1 - 0.35 Hz (Butterworth, zero-phase).
    2. Inhalation peak / Exhalation trough segmentation.
    """
    raw_data = sig.data
    fs = sig.fs

    if len(raw_data) < int(fs * 5):
        return CleanRESP(
            filtered=raw_data,
            peaks=np.array([], dtype=int),
            troughs=np.array([], dtype=int),
            resp_rate=0.0,
        )

    # 1. Bandpass filter 0.1 - 0.35 Hz (6 - 21 breaths/min)
    b, a = butter(N=2, Wn=[0.1, 0.35], btype="bandpass", fs=fs)
    filtered = filtfilt(b, a, raw_data)

    # 2. Peak / Trough segmentation
    try:
        rsp_signals, _ = nk.rsp_process(filtered, sampling_rate=int(fs))
        peaks = np.where(rsp_signals["RSP_Peaks"].values == 1)[0]
        troughs = np.where(rsp_signals["RSP_Troughs"].values == 1)[0]
        rates = rsp_signals["RSP_Rate"].values
        mean_rate = float(np.mean(rates)) if len(rates) > 0 else 0.0
    except Exception:
        peaks = np.array([], dtype=int)
        troughs = np.array([], dtype=int)
        mean_rate = 0.0

    return CleanRESP(
        filtered=filtered,
        peaks=peaks,
        troughs=troughs,
        resp_rate=mean_rate,
    )
