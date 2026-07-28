"""
Voice / Audio Resampling & Voice Activity Detection (VAD)
"""
from dataclasses import dataclass
from pathlib import Path
import librosa
import numpy as np


@dataclass(frozen=True)
class CleanVoice:
    audio_16k: np.ndarray            # 16 kHz resampled audio signal
    fs: float = 16000.0
    voiced_mask: np.ndarray = None   # Boolean mask of voiced segments
    vad_ratio: float = 0.0           # Fraction of audio containing speech


def clean_voice(audio_path: Path, target_sr: float = 16000.0) -> CleanVoice:
    """
    Loads audio, resamples to 16 kHz, and runs Voice Activity Detection (VAD).
    """
    if not audio_path.exists():
        return CleanVoice(
            audio_16k=np.array([], dtype=np.float32),
            fs=target_sr,
            voiced_mask=np.array([], dtype=bool),
            vad_ratio=0.0,
        )

    try:
        y, sr = librosa.load(audio_path, sr=int(target_sr))
    except Exception:
        return CleanVoice(
            audio_16k=np.array([], dtype=np.float32),
            fs=target_sr,
            voiced_mask=np.array([], dtype=bool),
            vad_ratio=0.0,
        )

    if len(y) == 0:
        return CleanVoice(
            audio_16k=y,
            fs=target_sr,
            voiced_mask=np.array([], dtype=bool),
            vad_ratio=0.0,
        )

    # Simple amplitude-based VAD thresholding
    rms = librosa.feature.rms(y=y, frame_length=512, hop_length=256)[0]
    thresh = float(np.percentile(rms, 25)) + 1e-4
    voiced_frames = rms > thresh
    
    # Expand frame mask back to audio sample length
    voiced_samples = np.repeat(voiced_frames, 256)[:len(y)]
    vad_ratio = float(np.mean(voiced_samples)) if len(voiced_samples) > 0 else 0.0

    return CleanVoice(
        audio_16k=y,
        fs=target_sr,
        voiced_mask=voiced_samples,
        vad_ratio=vad_ratio,
    )
