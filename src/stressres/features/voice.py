import librosa
import numpy as np
from stressres.clean.voice import CleanVoice
from stressres.types import WindowSpec


def extract_voice_features(clean: CleanVoice, spec: WindowSpec) -> dict[str, float | None]:
    """
    Extract 140-D handcrafted acoustic features (MFCCs, spectral centroid, pitch) for one window.
    """
    audio = clean.audio_16k
    fs = clean.fs
    i0 = int(spec.t_start * fs)
    i1 = int(spec.t_end * fs)

    w_audio = audio[i0:i1]

    if len(w_audio) < int(fs * 0.5):
        return {}

    feats = {}

    # 1. MFCCs (13 coefficients + deltas)
    mfcc = librosa.feature.mfcc(y=w_audio, sr=int(fs), n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

    for i in range(13):
        feats[f"mfcc_{i}_mean"] = float(np.mean(mfcc[i]))
        feats[f"mfcc_{i}_std"] = float(np.std(mfcc[i], ddof=1))
        feats[f"mfcc_d_{i}_mean"] = float(np.mean(mfcc_delta[i]))
        feats[f"mfcc_d2_{i}_mean"] = float(np.mean(mfcc_delta2[i]))

    # 2. Spectral Features
    cent = librosa.feature.spectral_centroid(y=w_audio, sr=int(fs))[0]
    bw = librosa.feature.spectral_bandwidth(y=w_audio, sr=int(fs))[0]
    rolloff = librosa.feature.spectral_rolloff(y=w_audio, sr=int(fs))[0]
    zcr = librosa.feature.zero_crossing_rate(y=w_audio)[0]

    feats["spectral_centroid_mean"] = float(np.mean(cent))
    feats["spectral_centroid_std"] = float(np.std(cent, ddof=1))
    feats["spectral_bandwidth_mean"] = float(np.mean(bw))
    feats["spectral_rolloff_mean"] = float(np.mean(rolloff))
    feats["zcr_mean"] = float(np.mean(zcr))

    return feats
