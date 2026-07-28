import argparse
import sys
from pathlib import Path
import pandas as pd

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from stressres.baseline.profiles import build_baseline_profile


def main():
    parser = argparse.ArgumentParser(description="Stage 4 Baseline Profiles CLI")
    parser.add_argument("--features", type=str, default="data/processed/features/wesad_ecg_features.parquet", nargs="?", help="Input features parquet path")
    parser.add_argument("--out", type=str, default="data/processed/baselines/baseline_profiles.parquet")
    args = parser.parse_args()

    feat_path = repo_root / args.features
    if not feat_path.exists():
        print(f"Error: Features file not found at {feat_path}")
        sys.exit(1)

    df = pd.read_parquet(feat_path)
    ignore_cols = {
        "dataset", "subject_id", "task", "window_id", "t_start", "t_end",
        "modality", "label_binary", "label_source", "is_baseline",
        "extractor_version", "config_hash", "quality", "quality_reason"
    }
    feature_cols = [c for c in df.columns if c not in ignore_cols]

    subjs = df["subject_id"].unique()
    modality = df["modality"].iloc[0] if "modality" in df.columns else "physio"

    rows = []
    print(f"Building Stage 4 baseline profiles for {len(subjs)} subjects...")

    for s in subjs:
        prof = build_baseline_profile(df, subject_id=s, modality=modality, feature_cols=feature_cols)
        row = {
            "subject_id": s,
            "modality": modality,
            "valid": prof.valid,
            "n_baseline_windows": prof.n_windows,
            "reason": prof.reason,
        }
        for fcol in feature_cols:
            row[f"med_{fcol}"] = prof.medians.get(fcol, None)
            row[f"mad_{fcol}"] = prof.mads.get(fcol, None)
        rows.append(row)

    out_df = pd.DataFrame(rows)
    out_path = repo_root / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_parquet(out_path, index=False)

    print("==================================================")
    print("STAGE 4 BASELINE PROFILES SUMMARY")
    print("==================================================")
    print(f"Total profiles created  : {len(out_df)}")
    print(f"Valid profiles count   : {out_df['valid'].sum()} / {len(out_df)}")
    print(f"Saved baseline profiles to: {out_path}")


if __name__ == "__main__":
    main()
