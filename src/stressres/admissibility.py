"""
Feature Admissibility Rules

Grounded in Baek & Cho (2021) and Munoz et al. (2015).
Ensures short windows or speaking tasks do not compute invalid physiological metrics (e.g. frequency-domain HRV during speech).
"""

HRV_MIN_DURATION = {
    'mean_hr': 30.0,
    'sd_hr': 30.0,
    'min_hr': 30.0,
    'max_hr': 30.0,
    'mean_rr': 30.0,
    'rmssd': 10.0,
    'pnn50': 10.0,
    'pnn20': 10.0,
    'sdnn': 30.0,
    'sdsd': 30.0,
    'cvnn': 30.0,
    'lf_power': 60.0,
    'hf_power': 60.0,
    'lf_hf_ratio': 60.0,
    'lf_norm': 60.0,
    'hf_norm': 60.0,
    'total_power': 60.0,
    'vlf_power': 60.0,
    'sd1': 10.0,
    'sd2': 30.0,
    'sd1_sd2': 30.0,
    'sample_entropy': 30.0,
}

STATIC_ONLY_FEATURES = {
    'sdnn',
    'lf_power',
    'hf_power',
    'lf_hf_ratio',
    'hf_norm',
    'lf_norm',
    'vlf_power',
    'total_power',
}

SPEAKING_TASKS = {
    'stressid': {'Speaking', 'Reading', 'Counting1', 'Counting2', 'Counting3', 'Math', 'Stroop'},
    'wesad': {'stress'},  # TSST involves speech
}


def admissible_features(modality: str, duration_s: float, task: str, dataset: str) -> frozenset[str]:
    """
    Returns the set of feature names physiologically valid for this window.
    """
    valid = set()
    is_speaking = task in SPEAKING_TASKS.get(dataset.lower(), set())

    if modality == 'ecg':
        for feat, min_dur in HRV_MIN_DURATION.items():
            if duration_s < min_dur:
                continue
            if is_speaking and feat in STATIC_ONLY_FEATURES:
                continue
            valid.add(feat)

    elif modality in ('eda', 'resp', 'face', 'voice'):
        # EDA, Resp, Face, Voice features are valid across standard window durations
        valid = {'all'}

    return frozenset(valid)
