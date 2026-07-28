from dataclasses import dataclass
import neurokit2 as nk
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.signal import butter, filtfilt
from stressres.types import Signal


@dataclass(frozen=True)
class CleanECG:
    filtered: np.ndarray             # 1-D clean ECG signal
    r_peaks: np.ndarray              # R-peak sample indices
    rr_intervals: np.ndarray         # Corrected RR intervals (seconds)
    rr_times: np.ndarray             # Times corresponding to RR intervals
    pct_ectopic: float               # Percentage of corrected ectopic beats
    n_valid_rr: int                  # Total count of valid RR intervals


def clean_ecg(sig: Signal) -> CleanECG:
    """
    Cleans ECG signal:
    1. Butterworth bandpass 0.5 - 40 Hz using zero-phase `filtfilt`.
    2. R-peak detection via NeuroKit2.
    3. Ectopic RR correction (5-neighbour median window, >20% threshold, cubic interpolation).
    """
    raw_data = sig.data
    fs = sig.fs

    if len(raw_data) < int(fs * 5):
        # Empty / tiny signal fallback
        return CleanECG(
            filtered=raw_data,
            r_peaks=np.array([], dtype=int),
            rr_intervals=np.array([], dtype=float),
            rr_times=np.array([], dtype=float),
            pct_ectopic=1.0,
            n_valid_rr=0,
        )

    # 1. Butterworth 0.5-40 Hz bandpass filter
    b, a = butter(N=3, Wn=[0.5, 40.0], btype="bandpass", fs=fs)
    filtered = filtfilt(b, a, raw_data)

    # 2. R-peak detection
    try:
        _, rpeaks_info = nk.ecg_peaks(filtered, sampling_rate=int(fs), method="neurokit")
        r_peaks = rpeaks_info.get("ECG_R_Peaks", np.array([], dtype=int))
    except Exception:
        r_peaks = np.array([], dtype=int)

    if len(r_peaks) < 3:
        return CleanECG(
            filtered=filtered,
            r_peaks=r_peaks,
            rr_intervals=np.array([], dtype=float),
            rr_times=np.array([], dtype=float),
            pct_ectopic=1.0,
            n_valid_rr=0,
        )

    # Calculate raw RR intervals (in seconds)
    rr_raw = np.diff(r_peaks) / fs
    rr_times = sig.t0 + r_peaks[1:] / fs

    # 3. Ectopic RR correction
    rr_corrected = np.copy(rr_raw)
    n_rr = len(rr_raw)
    ectopic_mask = np.zeros(n_rr, dtype=bool)

    for i in range(n_rr):
        i_min = max(0, i - 2)
        i_max = min(n_rr, i + 3)
        local_window = rr_raw[i_min:i_max]
        local_median = float(np.median(local_window))
        if local_median > 0:
            dev = abs(rr_raw[i] - local_median) / local_median
            if dev > 0.20:
                ectopic_mask[i] = True

    n_ectopic = int(np.sum(ectopic_mask))
    pct_ectopic = float(n_ectopic) / float(n_rr) if n_rr > 0 else 0.0

    # Cubic interpolation for ectopic beats
    if n_ectopic > 0 and n_rr > n_ectopic and (n_rr - n_ectopic) >= 4:
        valid_indices = np.where(~ectopic_mask)[0]
        ectopic_indices = np.where(ectopic_mask)[0]
        try:
            interp_vals = np.interp(ectopic_indices, valid_indices, rr_raw[valid_indices])
            rr_corrected[ectopic_indices] = interp_vals
        except Exception:
            pass

    return CleanECG(
        filtered=filtered,
        r_peaks=r_peaks,
        rr_intervals=rr_corrected,
        rr_times=rr_times,
        pct_ectopic=pct_ectopic,
        n_valid_rr=len(rr_corrected),
    )
