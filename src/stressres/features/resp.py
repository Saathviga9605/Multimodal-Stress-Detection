import numpy as np
from stressres.clean.resp import CleanRESP
from stressres.types import WindowSpec


def extract_resp_features(clean: CleanRESP, spec: WindowSpec) -> dict[str, float | None]:
    """
    Extract respiration features for one window.
    """
    fs = 700.0 if spec.dataset == "wesad" else 500.0
    i0 = int(spec.t_start * fs)
    i1 = int(spec.t_end * fs)

    peaks_in_w = clean.peaks[(clean.peaks >= i0) & (clean.peaks < i1)]
    troughs_in_w = clean.troughs[(clean.troughs >= i0) & (clean.troughs < i1)]

    if len(peaks_in_w) < 2 or len(troughs_in_w) < 2:
        return {
            "resp_rate": clean.resp_rate,
            "mean_inhale_dur": None, "sd_inhale_dur": None,
            "mean_exhale_dur": None, "sd_exhale_dur": None,
            "ie_ratio": None, "stretch_range": None,
            "rrv_rmssd": None, "rrv_sdbb": None,
        }

    # Inhale duration: peak time - preceding trough time
    inhale_durs = []
    exhale_durs = []

    for p in peaks_in_w:
        tr_prev = troughs_in_w[troughs_in_w < p]
        if len(tr_prev) > 0:
            inhale_durs.append((p - tr_prev[-1]) / fs)

    for tr in troughs_in_w:
        p_prev = peaks_in_w[peaks_in_w < tr]
        if len(p_prev) > 0:
            exhale_durs.append((tr - p_prev[-1]) / fs)

    mean_inhale = float(np.mean(inhale_durs)) if len(inhale_durs) > 0 else 0.0
    sd_inhale = float(np.std(inhale_durs, ddof=1)) if len(inhale_durs) > 1 else 0.0
    mean_exhale = float(np.mean(exhale_durs)) if len(exhale_durs) > 0 else 0.0
    sd_exhale = float(np.std(exhale_durs, ddof=1)) if len(exhale_durs) > 1 else 0.0

    ie_ratio = (mean_inhale / mean_exhale) if mean_exhale > 1e-4 else 1.0

    # Breath-to-breath interval variability (RRV)
    bb_intervals = np.diff(peaks_in_w) / fs
    if len(bb_intervals) > 1:
        drrv = np.diff(bb_intervals)
        rrv_rmssd = float(np.sqrt(np.mean(drrv ** 2))) if len(drrv) > 0 else 0.0
        rrv_sdbb = float(np.std(bb_intervals, ddof=1))
    else:
        rrv_rmssd, rrv_sdbb = 0.0, 0.0

    return {
        "resp_rate": clean.resp_rate,
        "mean_inhale_dur": mean_inhale,
        "sd_inhale_dur": sd_inhale,
        "mean_exhale_dur": mean_exhale,
        "sd_exhale_dur": sd_exhale,
        "ie_ratio": ie_ratio,
        "stretch_range": float(np.ptp(clean.filtered[i0:i1])) if i1 > i0 else 0.0,
        "rrv_rmssd": rrv_rmssd,
        "rrv_sdbb": rrv_sdbb,
    }
