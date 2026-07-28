import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from tqdm import tqdm

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from stressres.io.wesad import load_wesad
from stressres.io.stressid import load_stressid
from stressres.io.audio import load_stressid_audio
from stressres.io.video import load_stressid_video_frames
from stressres.clean.ecg import clean_ecg
from stressres.clean.eda import clean_eda
from stressres.clean.resp import clean_resp
from stressres.clean.voice import clean_voice, CleanVoice
from stressres.quality.sqi import compute_ecg_sqi, compute_eda_sqi, compute_resp_sqi
from stressres.windows.grid import build_window_specs_for_session
from stressres.features.ecg import extract_ecg_features
from stressres.features.eda import extract_eda_features
from stressres.features.resp import extract_resp_features
from stressres.features.voice import extract_voice_features
from stressres.provenance import get_provenance_metadata


def main():
    parser = argparse.ArgumentParser(description="Stage 3 Feature Extraction CLI")
    parser.add_argument("--dataset", type=str, required=True, choices=["wesad", "stressid"])
    parser.add_argument("--modality", type=str, default="ecg", choices=["ecg", "eda", "resp", "physio", "voice", "face"])
    parser.add_argument("--raw-dir", type=str, default="Datasets")
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    dataset_dir = repo_root / args.raw_dir / args.dataset
    if args.out is None:
        out_path = repo_root / "data" / "processed" / "features" / f"{args.dataset}_{args.modality}_features.parquet"
    else:
        out_path = repo_root / args.out

    prov = get_provenance_metadata(repo_root / "config")
    feature_rows = []

    print(f"Extracting Stage 3 features for {args.dataset.upper()} ({args.modality})...", flush=True)

    if args.dataset == "wesad":
        import yaml
        with open(repo_root / "config" / "subjects.yaml", "r") as f:
            subjs = yaml.safe_load(f)["wesad"]["subjects"]

        pbar = tqdm(subjs, desc="Processing WESAD Subjects", unit="subject")
        for s in pbar:
            pkl = dataset_dir / s / f"{s}.pkl"
            if not pkl.exists():
                continue
            
            pbar.set_postfix({"subject": s, "step": "loading"})
            sess = load_wesad(pkl)
            _extract_session_features(sess, args.modality, prov, feature_rows, pbar, s)

    elif args.dataset == "stressid":
        labels_csv = dataset_dir / "labels.csv"
        labels_df = pd.read_csv(labels_csv) if labels_csv.exists() else None
        self_assess_csv = dataset_dir / "self_assessments.csv"

        if args.modality == "voice":
            audio_dir = dataset_dir / "Audio"
            if audio_dir.exists():
                aud_files = [f for f in audio_dir.glob("**/*.wav") if not f.name.startswith("._")]
                subjs = sorted(list(set([f.stem.split("_")[0] for f in aud_files if "_" in f.stem])))

                pbar = tqdm(subjs, desc="Processing StressID Audio Subjects", unit="subject")
                for s in pbar:
                    pbar.set_postfix({"subject": s, "step": "loading"})
                    sess = load_stressid_audio(s, dataset_dir, labels_df)
                    _extract_session_features(sess, args.modality, prov, feature_rows, pbar, s)

        elif args.modality == "face":
            video_dir = dataset_dir / "Videos"
            if video_dir.exists():
                vid_files = [f for f in video_dir.glob("**/*.mp4") if not f.name.startswith("._")]
                subjs = sorted(list(set([f.stem.split("_")[0] for f in vid_files if "_" in f.stem])))

                pbar = tqdm(subjs, desc="Processing StressID Video Subjects", unit="subject")
                for s in pbar:
                    pbar.set_postfix({"subject": s, "step": "loading"})
                    sess = load_stressid_video_frames(s, dataset_dir, labels_df)
                    _extract_session_features(sess, args.modality, prov, feature_rows, pbar, s)

        else:
            physio_dir = dataset_dir / "Physiological"
            if physio_dir.exists():
                p_files = list(physio_dir.glob("**/*.txt")) + list(physio_dir.glob("**/*.csv"))
                subjs = sorted(list(set([f.stem.split("_")[0] for f in p_files if "_" in f.stem])))
                
                pbar = tqdm(subjs, desc="Processing StressID Physio Subjects", unit="subject")
                for s in pbar:
                    pbar.set_postfix({"subject": s, "step": "loading"})
                    sess = load_stressid(s, dataset_dir, labels_df, self_assess_csv)
                    _extract_session_features(sess, args.modality, prov, feature_rows, pbar, s)

    df = pd.DataFrame(feature_rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    print("\n==================================================", flush=True)
    print("STAGE 3 FEATURE EXTRACTION SUMMARY", flush=True)
    print("==================================================", flush=True)
    print(f"Extracted feature rows : {len(df)}", flush=True)
    if not df.empty:
        print(f"Feature columns count : {len(df.columns)}", flush=True)
    print(f"Saved feature dataset to: {out_path}", flush=True)


def _extract_session_features(sess, modality, prov, feature_rows, pbar, s):
    pbar.set_postfix({"subject": s, "step": "cleaning"})
    c_ecg = clean_ecg(sess.signals["ecg"]) if modality in ("ecg", "physio") and "ecg" in sess.signals else None
    c_eda = clean_eda(sess.signals["eda"]) if modality in ("eda", "physio") and "eda" in sess.signals else None
    c_resp = clean_resp(sess.signals["resp"]) if modality in ("resp", "physio") and "resp" in sess.signals else None
    c_voice = clean_voice(sess.signals["voice"]) if modality == "voice" and "voice" in sess.signals else None

    pbar.set_postfix({"subject": s, "step": "windowing"})
    if modality == "voice":
        window_s, stride = 5.0, 2.5
    elif modality == "face":
        window_s, stride = 10.0, 5.0
    else:
        window_s, stride = 60.0, 5.0 if sess.dataset == "wesad" else 30.0

    specs = build_window_specs_for_session(sess, modality=modality, window_s=window_s, stride_s=stride)

    pbar.set_postfix({"subject": s, "step": f"extracting {len(specs)} windows"})
    for sp in specs:
        row = {
            "dataset": sp.dataset,
            "subject_id": sp.subject_id,
            "task": sp.task,
            "window_id": sp.window_id,
            "t_start": sp.t_start,
            "t_end": sp.t_end,
            "modality": modality,
            "label_binary": sp.label_binary,
            "label_source": sp.label_source,
            "is_baseline": sp.is_baseline,
            "extractor_version": prov["git_sha"],
            "config_hash": prov["config_hash"],
        }

        if modality in ("ecg", "physio") and c_ecg:
            feats = extract_ecg_features(c_ecg, sp)
            sqi_res = compute_ecg_sqi(c_ecg)
            row.update(feats)
            row["quality"] = sqi_res.sqi
            row["quality_reason"] = sqi_res.reason

        elif modality == "eda" and c_eda:
            feats = extract_eda_features(c_eda, sp)
            sqi_res = compute_eda_sqi(c_eda)
            row.update(feats)
            row["quality"] = sqi_res.sqi
            row["quality_reason"] = sqi_res.reason

        elif modality == "resp" and c_resp:
            feats = extract_resp_features(c_resp, sp)
            sqi_res = compute_resp_sqi(c_resp)
            row.update(feats)
            row["quality"] = sqi_res.sqi
            row["quality_reason"] = sqi_res.reason

        elif modality == "voice" and c_voice:
            feats = extract_voice_features(c_voice, sp)
            row.update(feats)
            row["quality"] = 1.0 if c_voice.vad_ratio >= 0.2 else 0.0
            row["quality_reason"] = "" if c_voice.vad_ratio >= 0.2 else "Low VAD speech ratio"

        elif modality == "face":
            row["quality"] = 1.0
            row["quality_reason"] = ""

        feature_rows.append(row)


if __name__ == "__main__":
    main()
