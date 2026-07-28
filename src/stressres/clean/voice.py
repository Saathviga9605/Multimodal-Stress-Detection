"""
Voice / Audio Resampling & Voice Activity Detection (VAD)
"""
from dataclasses import dataclass
from pathlib import Path
import librosa
import numpy as np
from stressres.types import Signal


@dataclass(frozen=True)
class CleanVoice:
    audio_16k: np.ndarray            # 16 kHz resampled audio signal
    fs: float = 16000.0
    voiced_mask: np.ndarray = None   # Boolean mask of voiced segments
    vad_ratio: float = 0.0           # Fraction of audio containing speech


def clean_voice(input_data: Signal | Path | np.ndarray, target_sr: float = 16000.0) -> CleanVoice:
    """
    Loads/resamples audio to 16 kHz and runs Voice Activity Detection (VAD).
    """
    if isinstance(input_data, Signal):
        y = input_data.data.astype(np.float32)
        sr = input_data.fs
        if sr != target_sr:
            y = librosa.resample(y, orig_sr=int(sr), target_sr=int(target_sr))
            sr = target_sr

    elif isinstance(input_data, (str, Path)):
        p = Path(input_data)
        if not p.exists():
            return CleanVoice(
                audio_16k=np.array([], dtype=np.float32),
                fs=target_sr,
                voiced_mask=np.array([], dtype=bool),
                vad_ratio=0.0,
            )
        try:
            y, sr = librosa.load(p, sr=int(target_sr))
        except Exception:
            return CleanVoice(
                audio_16k=np.array([], dtype=np.float32),
                fs=target_sr,
                voiced_mask=np.array([], dtype=bool),
                vad_ratio=0.0,
            )
    elif isinstance(input_data, np.ndarray):
        y = input_data.astype(np.float32)
        sr = target_sr
    else:
        return CleanVoice(
            audio_16k=np.array([], dtype=np.float32),
            fs=target_sr,
            voiced_mask=np.array([], dtype=bool),
            vad_ratio=0.0,
        )

    if len(y) == 0:
        return CleanVoice(
            audio_16k=np.array([], dtype=np.float32),
            fs=target_sr,
            voiced_mask=np.array([], dtype=bool),
            vad_ratio=0.0,
        )

    # RMS energy VAD thresholding
    frame_length = int(target_sr * 0.03)  # 30 ms
    hop_length = int(target_sr * 0.01)    # 10 ms
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

    # Threshold speech above 10% of max energy
    threshold = max(0.01, 0.1 * np.max(rms)) if len(rms) > 0 else 0.01
    voiced_frames = rms > threshold

    voiced_samples = np.repeat(voiced_frames, hop_length)[: len(y)]
    vad_ratio = float(np.mean(voiced_samples)) if len(voiced_samples) > 0 else 0.0

    return CleanVoice(
        audio_16k=y,
        fs=target_sr,
        voiced_mask=voiced_samples,
        vad_ratio=vad_ratio,
    )
