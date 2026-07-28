import numpy as np
from stressres.clean.eda import CleanEDA
from stressres.types import WindowSpec


def extract_eda_features(clean: CleanEDA, spec: WindowSpec) -> dict[str, float | None]:
    """
    Extract electrodermal features for one window.
    """
    fs = clean.fs
    i0 = int(spec.t_start * fs)
    i1 = int(spec.t_end * fs)

    scl = clean.tonic[i0:i1]
    scr = clean.phasic[i0:i1]

    if len(scl) < 4:
        return {
            "mean_scl": None, "sd_scl": None, "slope_scl": None, "range_scl": None,
            "mean_scr": None, "sd_scr": None, "auc_scr": None,
            "n_scr_peaks": None, "scr_rate_per_min": None, "mean_scr_amplitude": None,
            "sum_scr_amplitude": None,
        }

    duration_min = (spec.t_end - spec.t_start) / 60.0

    # Tonic features
    mean_scl = float(np.mean(scl))
    sd_scl = float(np.std(scl, ddof=1)) if len(scl) > 1 else 0.0
    range_scl = float(np.ptp(scl))

    # Slope SCL via linear fit
    x = np.arange(len(scl)) / fs
    slope_scl = float(np.polyfit(x, scl, 1)[0]) if len(scl) > 1 else 0.0

    # Phasic features
    mean_scr = float(np.mean(scr))
    sd_scr = float(np.std(scr, ddof=1)) if len(scr) > 1 else 0.0
    auc_scr = float(np.trapz(np.maximum(0, scr), x=x))

    # SCR Peak Events within window
    peaks_in_w = clean.scr_peaks[(clean.scr_peaks >= i0) & (clean.scr_peaks < i1)]
    n_peaks = len(peaks_in_w)
    scr_rate = float(n_peaks) / duration_min if duration_min > 0 else 0.0

    if n_peaks > 0:
        amps = clean.phasic[peaks_in_w]
        mean_amp = float(np.mean(amps))
        sum_amp = float(np.sum(amps))
    else:
        mean_amp = 0.0
        sum_amp = 0.0

    return {
        "mean_scl": mean_scl,
        "sd_scl": sd_scl,
        "slope_scl": slope_scl,
        "range_scl": range_scl,
        "mean_scr": mean_scr,
        "sd_scr": sd_scr,
        "auc_scr": auc_scr,
        "n_scr_peaks": n_peaks,
        "scr_rate_per_min": scr_rate,
        "mean_scr_amplitude": mean_amp,
        "sum_scr_amplitude": sum_amp,
    }
