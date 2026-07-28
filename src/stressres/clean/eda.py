from dataclasses import dataclass
import neurokit2 as nk
import numpy as np
from scipy.signal import butter, filtfilt, resample_poly
from stressres.types import Signal


@dataclass(frozen=True)
class CleanEDA:
    filtered: np.ndarray             # 1-D clean EDA signal (at target_fs)
    tonic: np.ndarray                # SCL (Skin Conductance Level)
    phasic: np.ndarray               # SCR (Skin Conductance Response)
    scr_peaks: np.ndarray            # SCR peak sample indices
    fs: float                        # Output sampling rate (e.g. 8 Hz)


def clean_eda(sig: Signal, target_fs: float = 8.0, eda_method: str = "highpass") -> CleanEDA:
    """
    Cleans EDA signal:
    1. Lowpass filter at 1.0 Hz (Butterworth).
    2. Downsample to target_fs (8.0 Hz) for efficiency.
    3. Decompose into tonic (SCL) and phasic (SCR) via NeuroKit2 eda_phasic.
    4. Detect SCR peak events (> 0.01 uS amplitude threshold).
    """
    raw_data = sig.data
    fs = sig.fs

    if len(raw_data) < int(fs * 3):
        return CleanEDA(
            filtered=raw_data,
            tonic=np.zeros_like(raw_data),
            phasic=np.zeros_like(raw_data),
            scr_peaks=np.array([], dtype=int),
            fs=fs,
        )

    # 1. Lowpass filter at 1.0 Hz
    b, a = butter(N=2, Wn=1.0, btype="lowpass", fs=fs)
    filtered_native = filtfilt(b, a, raw_data)

    # 2. Downsample to 8 Hz if native rate is higher (e.g. 500 Hz or 700 Hz)
    if fs > target_fs:
        up = int(target_fs)
        down = int(fs)
        # Simplify fraction ratio
        gcd = np.gcd(up, down)
        up //= gcd
        down //= gcd
        filtered = resample_poly(filtered_native, up, down)
        out_fs = target_fs
    else:
        filtered = filtered_native
        out_fs = fs

    # 3. Tonic / Phasic decomposition
    try:
        eda_signals, _ = nk.eda_phasic(filtered, sampling_rate=int(out_fs), method=eda_method)
        tonic = eda_signals["EDA_Tonic"].values
        phasic = eda_signals["EDA_Phasic"].values
    except Exception:
        # Fallback highpass filter decomposition
        b_hp, a_hp = butter(N=2, Wn=0.05, btype="highpass", fs=out_fs)
        phasic = filtfilt(b_hp, a_hp, filtered)
        tonic = filtered - phasic

    # 4. SCR peak detection (> 0.01 uS threshold)
    try:
        scr_info, _ = nk.eda_peaks(phasic, sampling_rate=int(out_fs), amplitude_min=0.01)
        scr_peaks = scr_info.get("SCR_Peaks", np.array([], dtype=int))
    except Exception:
        scr_peaks = np.array([], dtype=int)

    return CleanEDA(
        filtered=filtered,
        tonic=tonic,
        phasic=phasic,
        scr_peaks=scr_peaks,
        fs=out_fs,
    )
