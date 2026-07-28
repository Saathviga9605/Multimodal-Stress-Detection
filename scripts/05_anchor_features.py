import argparse
import sys
from pathlib import Path
import pandas as pd

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from stressres.baseline.profiles import BaselineProfile, anchor_features


def main():
    parser = argparse.ArgumentParser(description="Stage 5 Baseline Feature Anchoring CLI")
    parser.add_argument("--features", type=str, default="data/processed/features/wesad_ecg_features.parquet", nargs="?", help="Input raw features parquet path")
    parser.add_argument("--profiles", type=str, default="data/processed/baselines/baseline_profiles.parquet", nargs="?", help="Baseline profiles parquet path")
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    feat_path = repo_root / args.features
    prof_path = repo_root / args.profiles

    if not feat_path.exists() or not prof_path.exists():
        print("Error: Feature or profile file not found.")
        sys.exit(1)

    df_feats = pd.read_parquet(feat_path)
    df_profs = pd.read_parquet(prof_path)

    ignore_cols = {
        "dataset", "subject_id", "task", "window_id", "t_start", "t_end",
        "modality", "label_binary", "label_source", "is_baseline",
        "extractor_version", "config_hash", "quality", "quality_reason"
    }
    feature_cols = [c for c in df_feats.columns if c not in ignore_cols and not c.endswith("_raw") and not c.endswith("_anch")]

    anchored_dfs = []

    for s, s_df in df_feats.groupby("subject_id"):
        prof_row = df_profs[df_profs["subject_id"] == s]
        if prof_row.empty:
            prof = BaselineProfile(subject_id=s, modality="physio", valid=False, n_windows=0, reason="profile_missing")
        else:
            p_row = prof_row.iloc[0]
            valid = bool(p_row["valid"])
            meds = {c: p_row[f"med_{c}"] for c in feature_cols if f"med_{c}" in p_row and pd.notna(p_row[f"med_{c}"])}
            mads = {c: p_row[f"mad_{c}"] for c in feature_cols if f"mad_{c}" in p_row and pd.notna(p_row[f"mad_{c}"])}
            prof = BaselineProfile(subject_id=s, modality=p_row["modality"], valid=valid, n_windows=int(p_row["n_baseline_windows"]), medians=meds, mads=mads)

        s_anch = anchor_features(s_df, prof, feature_cols)
        anchored_dfs.append(s_anch)

    final_df = pd.concat(anchored_dfs, ignore_index=True)

    if args.out is None:
        out_path = feat_path.parent / f"{feat_path.stem}_anchored.parquet"
    else:
        out_path = repo_root / args.out

    out_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_parquet(out_path, index=False)

    print("==================================================")
    print("STAGE 5 FEATURE ANCHORING SUMMARY")
    print("==================================================")
    print(f"Total anchored rows : {len(final_df)}")
    print(f"Total columns emitted: {len(final_df.columns)}")
    print(f"Saved anchored dataset to: {out_path}")


if __name__ == "__main__":
    main()
