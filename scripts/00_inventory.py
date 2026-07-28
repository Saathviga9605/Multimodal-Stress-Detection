import argparse
import sys
from pathlib import Path
import pandas as pd
import yaml

# Add src to pythonpath
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))


def load_subjects_manifest(config_path: Path) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def inventory_stressid(raw_root: Path, manifest: dict) -> pd.DataFrame:
    rows = []
    stressid_cfg = manifest.get("stressid", {})
    physio_dir = raw_root / "Physiological"
    video_dir = raw_root / "Videos"
    audio_dir = raw_root / "Audio"

    # Physio Inventory
    if physio_dir.exists():
        physio_files = list(physio_dir.glob("**/*.txt")) + list(physio_dir.glob("**/*.csv"))
        for p_file in physio_files:
            stem = p_file.stem
            parts = stem.split("_")
            if len(parts) >= 2:
                subject_id, task = parts[0], parts[1]
                rows.append({
                    "dataset": "stressid",
                    "subject_id": subject_id,
                    "task": task,
                    "modality": "physio",
                    "file_path": str(p_file),
                    "size_bytes": p_file.stat().st_size,
                })

    # Video Inventory
    if video_dir.exists():
        vid_files = [f for f in video_dir.glob("**/*.mp4") if not f.name.startswith("._")]
        for vid_file in vid_files:
            stem = vid_file.stem
            parts = stem.split("_")
            if len(parts) >= 2:
                subject_id, task = parts[0], parts[1]
                rows.append({
                    "dataset": "stressid",
                    "subject_id": subject_id,
                    "task": task,
                    "modality": "video",
                    "file_path": str(vid_file),
                    "size_bytes": vid_file.stat().st_size,
                })

    # Audio Inventory
    if audio_dir.exists():
        aud_files = [f for f in audio_dir.glob("**/*.wav") if not f.name.startswith("._")]
        for aud_file in aud_files:
            stem = aud_file.stem
            parts = stem.split("_")
            if len(parts) >= 2:
                subject_id, task = parts[0], parts[1]
                rows.append({
                    "dataset": "stressid",
                    "subject_id": subject_id,
                    "task": task,
                    "modality": "audio",
                    "file_path": str(aud_file),
                    "size_bytes": aud_file.stat().st_size,
                })

    df = pd.DataFrame(rows)
    return df


def inventory_wesad(raw_root: Path, manifest: dict) -> pd.DataFrame:
    rows = []
    wesad_cfg = manifest.get("wesad", {})
    expected_subjects = wesad_cfg.get("subjects", [])

    for subj in expected_subjects:
        subj_dir = raw_root / subj
        pkl_path = subj_dir / f"{subj}.pkl"
        if pkl_path.exists():
            rows.append({
                "dataset": "wesad",
                "subject_id": subj,
                "task": "all",
                "modality": "physio_chest_and_wrist",
                "file_path": str(pkl_path),
                "size_bytes": pkl_path.stat().st_size,
            })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Stage 0 Raw Inventory Script")
    parser.add_argument("--config", type=str, default="config/subjects.yaml")
    parser.add_argument("--datasets-dir", type=str, default="Datasets")
    parser.add_argument("--out", type=str, default="data/processed/manifests/inventory.parquet")
    args = parser.parse_args()

    config_path = repo_root / args.config
    manifest = load_subjects_manifest(config_path)
    datasets_root = repo_root / args.datasets_dir

    df_wesad = inventory_wesad(datasets_root / "wesad", manifest)
    df_stressid = inventory_stressid(datasets_root / "stressid", manifest)

    df_all = pd.concat([df_wesad, df_stressid], ignore_index=True)

    out_path = repo_root / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_all.to_parquet(out_path, index=False)

    print("==================================================")
    print("STAGE 0 INVENTORY SUMMARY")
    print("==================================================")
    if not df_wesad.empty:
        w_subjs = df_wesad["subject_id"].nunique()
        print(f"WESAD physio : {w_subjs} subjects, {len(df_wesad)} files")
    
    if not df_stressid.empty:
        for mod in ["physio", "video", "audio"]:
            sub_df = df_stressid[df_stressid["modality"] == mod]
            n_sub = sub_df["subject_id"].nunique() if not sub_df.empty else 0
            n_rec = len(sub_df)
            print(f"STRESSID {mod:<6} : {n_sub} subjects, {n_rec} recordings")

    print(f"\nSaved inventory manifest to: {out_path}")


if __name__ == "__main__":
    main()
