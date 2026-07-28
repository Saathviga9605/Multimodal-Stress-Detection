import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from stressres.models.unimodal.physio_classifier import UnimodalPhysioClassifier
from stressres.models.fusion.decision_level import LateDecisionFusion


def evaluate_dataset_fusion(dataset: str, feat_dir: Path):
    print(f"\n==================================================")
    print(f"EVALUATING MULTIMODAL LATE FUSION FOR {dataset.upper()}")
    print("==================================================")

    prob_dict = {}
    common_y = None

    for mod in ["ecg", "eda", "resp"]:
        feat_path = feat_dir / f"{dataset}_{mod}_features_anchored.parquet"
        if not feat_path.exists():
            feat_path = feat_dir / f"{dataset}_{mod}_features.parquet"

        if feat_path.exists():
            df = pd.read_parquet(feat_path)
            clf = UnimodalPhysioClassifier(model_type="rf", n_estimators=100)
            res = clf.fit_predict_loso(df)

            print(f"  Unimodal {mod.upper():<5} -> Accuracy: {res['accuracy']:.2%}, F1: {res['f1_score']:.4f}")
            prob_dict[mod] = res["probabilities"]
            if common_y is None:
                common_y = df.dropna(subset=["label_binary"])["label_binary"].values
        else:
            print(f"  Unimodal {mod.upper():<5} -> Feature file not found ({feat_path.name})")

    if not prob_dict or common_y is None:
        print(f"Skipping fusion for {dataset.upper()}: Insufficient modality feature files.")
        return

    # Perform Late Decision Average Fusion
    fuser = LateDecisionFusion(rule="average")
    fusion_res = fuser.evaluate_fusion(prob_dict, common_y)

    print("\n--------------------------------------------------")
    print(f"{dataset.upper()} MULTIMODAL LATE DECISION FUSION SUMMARY")
    print("--------------------------------------------------")
    print(f"Average Rule Fusion -> Accuracy: {fusion_res['accuracy']:.2%}, F1: {fusion_res['f1_score']:.4f}")
    print("--------------------------------------------------")


def main():
    parser = argparse.ArgumentParser(description="Multimodal Decoupled Late Decision Fusion CLI")
    parser.add_argument("--dataset", type=str, default="all", choices=["wesad", "stressid", "all"])
    args = parser.parse_args()

    feat_dir = repo_root / "data" / "processed" / "features"

    if args.dataset == "all":
        for ds in ["wesad", "stressid"]:
            evaluate_dataset_fusion(ds, feat_dir)
    else:
        evaluate_dataset_fusion(args.dataset, feat_dir)


if __name__ == "__main__":
    main()
