import argparse
import sys
from pathlib import Path
import pandas as pd
import yaml

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from stressres.io.wesad import load_wesad
from stressres.io.stressid import load_stressid
from stressres.windows.grid import build_window_specs_for_session


def main():
    parser = argparse.ArgumentParser(description="Stage 2 Window Index Builder")
    parser.add_argument("--dataset", type=str, required=True, choices=["wesad", "stressid"])
    parser.add_argument("--modality", type=str, default="ecg")
    parser.add_argument("--raw-dir", type=str, default="Datasets")
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    dataset_dir = repo_root / args.raw_dir / args.dataset
    if args.out is None:
        out_path = repo_root / "data" / "processed" / "index" / f"{args.dataset}_{args.modality}_index.parquet"
    else:
        out_path = repo_root / args.out

    specs = []
    print(f"Building Stage 2 window index for {args.dataset.upper()} ({args.modality})...")

    if args.dataset == "wesad":
        with open(repo_root / "config" / "subjects.yaml", "r") as f:
            subjs = yaml.safe_load(f)["wesad"]["subjects"]

        for s in subjs:
            pkl = dataset_dir / s / f"{s}.pkl"
            if pkl.exists():
                sess = load_wesad(pkl)
                w_specs = build_window_specs_for_session(sess, modality=args.modality, window_s=60.0, stride_s=5.0, trim_onset_s=30.0)
                specs.extend(w_specs)

    else:
        # StressID subjects
        labels_csv = dataset_dir / "labels.csv"
        labels_df = pd.read_csv(labels_csv) if labels_csv.exists() else None
        self_assess_csv = dataset_dir / "self_assessments.csv"

        physio_dir = dataset_dir / "Physiological"
        if physio_dir.exists():
            p_files = list(physio_dir.glob("**/*.txt")) + list(physio_dir.glob("**/*.csv"))
            subjs = sorted(list(set([f.stem.split("_")[0] for f in p_files if "_" in f.stem])))
            for s in subjs:
                sess = load_stressid(s, dataset_dir, labels_df, self_assess_csv)
                w_specs = build_window_specs_for_session(sess, modality=args.modality, window_s=60.0, stride_s=30.0, trim_onset_s=0.0)
                specs.extend(w_specs)

    rows = []
    for sp in specs:
        rows.append({
            "dataset": sp.dataset,
            "subject_id": sp.subject_id,
            "task": sp.task,
            "modality": sp.modality,
            "window_id": sp.window_id,
            "t_start": sp.t_start,
            "t_end": sp.t_end,
            "label_binary": sp.label_binary,
            "label_source": sp.label_source,
            "is_baseline": sp.is_baseline,
            "admissible": ",".join(sp.admissible),
        })

    df = pd.DataFrame(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    print("==================================================")
    print("STAGE 2 WINDOW INDEX SUMMARY")
    print("==================================================")
    print(f"Total window specs built : {len(df)}")
    if not df.empty:
        print(f"Subjects represented     : {df['subject_id'].nunique()}")
        print(f"Class balance (label=1)  : {df['label_binary'].mean():.1%}")
    print(f"Saved window index to: {out_path}")


if __name__ == "__main__":
    main()
