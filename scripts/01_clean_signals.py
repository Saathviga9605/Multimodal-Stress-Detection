import argparse
import sys
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from stressres.io.wesad import load_wesad
from stressres.io.stressid import load_stressid
from stressres.clean.ecg import clean_ecg
from stressres.clean.eda import clean_eda
from stressres.clean.resp import clean_resp


def main():
    parser = argparse.ArgumentParser(description="Stage 1 Signal Cleaning CLI")
    parser.add_argument("--dataset", type=str, required=True, choices=["wesad", "stressid"])
    parser.add_argument("--subject", type=str, required=True, help="Subject ID (e.g. S2 or 2ea4)")
    parser.add_argument("--raw-dir", type=str, default="Datasets")
    parser.add_argument("--out-dir", type=str, default="data/processed/clean")
    args = parser.parse_args()

    raw_root = repo_root / args.raw_dir / args.dataset
    out_dir = repo_root / args.out_dir / args.dataset / args.subject
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Cleaning signals for {args.dataset.upper()} subject {args.subject}...")

    if args.dataset == "wesad":
        pkl_path = raw_root / args.subject / f"{args.subject}.pkl"
        session = load_wesad(pkl_path)
    else:
        labels_df = None
        labels_csv = repo_root / args.raw_dir / "stressid" / "labels.csv"
        if labels_csv.exists():
            import pandas as pd
            labels_df = pd.read_csv(labels_csv)
        self_assess_csv = repo_root / args.raw_dir / "stressid" / "self_assessments.csv"
        session = load_stressid(args.subject, raw_root, labels_df, self_assess_csv)

    # Clean available signals
    if "ecg" in session.signals:
        c_ecg = clean_ecg(session.signals["ecg"])
        np.savez_compressed(
            out_dir / "ecg.npz",
            filtered=c_ecg.filtered,
            r_peaks=c_ecg.r_peaks,
            rr_intervals=c_ecg.rr_intervals,
            rr_times=c_ecg.rr_times,
            pct_ectopic=c_ecg.pct_ectopic,
            n_valid_rr=c_ecg.n_valid_rr,
        )
        print(f"  ECG cleaned: {len(c_ecg.r_peaks)} peaks, ectopic={c_ecg.pct_ectopic:.1%}")

    if "eda" in session.signals:
        c_eda = clean_eda(session.signals["eda"], target_fs=8.0)
        np.savez_compressed(
            out_dir / "eda.npz",
            filtered=c_eda.filtered,
            tonic=c_eda.tonic,
            phasic=c_eda.phasic,
            scr_peaks=c_eda.scr_peaks,
            fs=c_eda.fs,
        )
        print(f"  EDA cleaned: {len(c_eda.scr_peaks)} SCR peaks detected")

    if "resp" in session.signals:
        c_resp = clean_resp(session.signals["resp"])
        np.savez_compressed(
            out_dir / "resp.npz",
            filtered=c_resp.filtered,
            peaks=c_resp.peaks,
            troughs=c_resp.troughs,
            resp_rate=c_resp.resp_rate,
        )
        print(f"  RESP cleaned: mean rate = {c_resp.resp_rate:.1f} breaths/min")

    print(f"Stage 1 outputs saved to: {out_dir}")


if __name__ == "__main__":
    main()
