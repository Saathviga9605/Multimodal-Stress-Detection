import neurokit2 as nk
import numpy as np
from scipy.signal import welch
from stressres.clean.ecg import CleanECG
from stressres.types import WindowSpec


def extract_ecg_features(clean: CleanECG, spec: WindowSpec) -> dict[str, float | None]:
    """
    Extract cardiac features for one window.
    Only computes features specified in spec.admissible.
    """
    feats: dict[str, float | None] = {}
    adm = spec.admissible

    # Mask RR intervals belonging to this window
    mask = (clean.rr_times >= spec.t_start) & (clean.rr_times <= spec.t_end)
    rrs = clean.rr_intervals[mask]

    if len(rrs) < 5:
        # Null fill if insufficient RR intervals
        all_feats = [
            "mean_hr", "sd_hr", "min_hr", "max_hr", "mean_rr",
            "rmssd", "sdnn", "pnn20", "pnn50", "sdsd", "cvnn",
            "lf_power", "hf_power", "lf_hf_ratio", "lf_norm", "hf_norm", "total_power",
            "sd1", "sd2", "sd1_sd2", "sample_entropy"
        ]
        return {f: None for f in all_feats}

    hrs = 60.0 / rrs

    # Time domain HR metrics
    if "mean_hr" in adm:
        feats["mean_hr"] = float(np.mean(hrs))
    else:
        feats["mean_hr"] = None

    if "sd_hr" in adm:
        feats["sd_hr"] = float(np.std(hrs, ddof=1)) if len(hrs) > 1 else 0.0
    else:
        feats["sd_hr"] = None

    if "min_hr" in adm:
        feats["min_hr"] = float(np.min(hrs))
    else:
        feats["min_hr"] = None

    if "max_hr" in adm:
        feats["max_hr"] = float(np.max(hrs))
    else:
        feats["max_hr"] = None

    if "mean_rr" in adm:
        feats["mean_rr"] = float(np.mean(rrs))
    else:
        feats["mean_rr"] = None

    # Time domain HRV metrics
    if "rmssd" in adm:
        drr = np.diff(rrs)
        feats["rmssd"] = float(np.sqrt(np.mean(drr ** 2))) if len(drr) > 0 else None
    else:
        feats["rmssd"] = None

    if "sdnn" in adm:
        feats["sdnn"] = float(np.std(rrs, ddof=1)) if len(rrs) > 1 else None
    else:
        feats["sdnn"] = None

    if "pnn50" in adm:
        drr_ms = np.abs(np.diff(rrs)) * 1000.0
        feats["pnn50"] = float(np.mean(drr_ms > 50.0)) if len(drr_ms) > 0 else None
    else:
        feats["pnn50"] = None

    if "pnn20" in adm:
        drr_ms = np.abs(np.diff(rrs)) * 1000.0
        feats["pnn20"] = float(np.mean(drr_ms > 20.0)) if len(drr_ms) > 0 else None
    else:
        feats["pnn20"] = None

    if "sdsd" in adm:
        drr = np.diff(rrs)
        feats["sdsd"] = float(np.std(drr, ddof=1)) if len(drr) > 1 else None
    else:
        feats["sdsd"] = None

    if "cvnn" in adm:
        feats["cvnn"] = (feats["sdnn"] / feats["mean_rr"]) if (feats["sdnn"] and feats["mean_rr"]) else None
    else:
        feats["cvnn"] = None

    # Frequency domain HRV metrics (Welch PSD)
    freq_keys = ["lf_power", "hf_power", "lf_hf_ratio", "lf_norm", "hf_norm", "total_power"]
    if any(k in adm for k in freq_keys):
        try:
            # Resample RR series to 4 Hz uniform grid for FFT/Welch
            t_rel = clean.rr_times[mask] - spec.t_start
            t_grid = np.arange(0, spec.t_end - spec.t_start, 0.25)
            rrs_interp = np.interp(t_grid, t_rel, rrs)

            freqs, psd = welch(rrs_interp, fs=4.0, nperseg=min(len(rrs_interp), 256))

            lf_mask = (freqs >= 0.04) & (freqs < 0.15)
            hf_mask = (freqs >= 0.15) & (freqs < 0.40)

            lf_power = float(np.trapz(psd[lf_mask], freqs[lf_mask])) if np.any(lf_mask) else 0.0
            hf_power = float(np.trapz(psd[hf_mask], freqs[hf_mask])) if np.any(hf_mask) else 0.0
            total_power = float(np.trapz(psd, freqs))

            feats["lf_power"] = lf_power if "lf_power" in adm else None
            feats["hf_power"] = hf_power if "hf_power" in adm else None
            feats["total_power"] = total_power if "total_power" in adm else None
            feats["lf_hf_ratio"] = (lf_power / hf_power) if (hf_power > 1e-8 and "lf_hf_ratio" in adm) else None

            denom = (lf_power + hf_power) + 1e-8
            feats["lf_norm"] = (lf_power / denom) if "lf_norm" in adm else None
            feats["hf_norm"] = (hf_power / denom) if "hf_norm" in adm else None
        except Exception:
            for k in freq_keys:
                feats[k] = None
    else:
        for k in freq_keys:
            feats[k] = None

    # Non-linear HRV
    if "sd1" in adm or "sd2" in adm:
        drr = np.diff(rrs)
        if len(drr) > 1:
            sd1 = float(np.sqrt(0.5 * np.var(drr, ddof=1)))
            sd2 = float(np.sqrt(2.0 * np.var(rrs, ddof=1) - 0.5 * np.var(drr, ddof=1)))
            feats["sd1"] = sd1 if "sd1" in adm else None
            feats["sd2"] = sd2 if "sd2" in adm else None
            feats["sd1_sd2"] = (sd1 / sd2) if (sd2 > 1e-8 and "sd1_sd2" in adm) else None
        else:
            feats["sd1"], feats["sd2"], feats["sd1_sd2"] = None, None, None
    else:
        feats["sd1"], feats["sd2"], feats["sd1_sd2"] = None, None, None

    feats["sample_entropy"] = None  # Optional complex non-linear metric

    return feats
