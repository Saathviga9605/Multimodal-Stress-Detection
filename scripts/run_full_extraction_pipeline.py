import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
python_exe = sys.executable


def run_step(cmd_args: list[str], title: str):
    print("\n" + "=" * 60)
    print(f"PIPELINE STEP: {title}")
    print("=" * 60)
    cmd = [python_exe] + cmd_args
    res = subprocess.run(cmd, cwd=repo_root)
    if res.returncode != 0:
        print(f"\n❌ Step failed: {title}")
        sys.exit(res.returncode)


def main():
    print("==================================================")
    print("STARTING END-TO-END MULTIMODAL FEATURE PIPELINE")
    print("==================================================")

    # 1. Stage 0 Inventory Check
    run_step(["scripts/00_inventory.py"], "Stage 0 Raw File Inventory Check")

    # 2. WESAD Multimodal Physio Extraction (ECG, EDA, RESP)
    for mod in ["ecg", "eda", "resp"]:
        run_step(
            ["scripts/03_extract_features.py", "--dataset", "wesad", "--modality", mod],
            f"WESAD {mod.upper()} Feature Extraction",
        )

    # 3. WESAD Baseline Profiles & Anchoring
    run_step(
        ["scripts/04_build_baseline_profiles.py", "--features", "data/processed/features/wesad_ecg_features.parquet", "--out", "data/processed/baselines/wesad_ecg_profiles.parquet"],
        "WESAD ECG Baseline Profiles",
    )
    run_step(
        ["scripts/05_anchor_features.py", "--features", "data/processed/features/wesad_ecg_features.parquet", "--profiles", "data/processed/baselines/wesad_ecg_profiles.parquet", "--out", "data/processed/features/wesad_ecg_features_anchored.parquet"],
        "WESAD ECG Baseline Anchoring",
    )

    # 4. StressID Multimodal Physio Extraction (ECG, EDA, RESP) across 65 subjects
    stressid_raw = repo_root / "Datasets" / "stressid" / "Physiological"
    if stressid_raw.exists():
        for mod in ["ecg", "eda", "resp"]:
            run_step(
                ["scripts/03_extract_features.py", "--dataset", "stressid", "--modality", mod],
                f"StressID {mod.upper()} Feature Extraction",
            )

        run_step(
            ["scripts/04_build_baseline_profiles.py", "--features", "data/processed/features/stressid_ecg_features.parquet", "--out", "data/processed/baselines/stressid_ecg_profiles.parquet"],
            "StressID ECG Baseline Profiles",
        )
        run_step(
            ["scripts/05_anchor_features.py", "--features", "data/processed/features/stressid_ecg_features.parquet", "--profiles", "data/processed/baselines/stressid_ecg_profiles.parquet", "--out", "data/processed/features/stressid_ecg_features_anchored.parquet"],
            "StressID ECG Baseline Anchoring",
        )

    # 5. Automated Test Suite Verification
    run_step(["-m", "pytest", "tests/"], "Automated Test Suite Verification (pytest)")

    # 6. WESAD Step 4 Benchmark Evaluation Gate
    run_step(["scripts/eval_loso_benchmark.py", "--features", "data/processed/features/wesad_ecg_features_anchored.parquet"], "WESAD Step 4 LOSO Benchmark Evaluation Gate")

    # 7. StressID Physio Benchmark Evaluation Gate
    if (repo_root / "data/processed/features/stressid_ecg_features_anchored.parquet").exists():
        run_step(["scripts/eval_loso_benchmark.py", "--features", "data/processed/features/stressid_ecg_features_anchored.parquet"], "StressID Physio LOSO Benchmark Evaluation Gate")

    print("\n==================================================")
    print("🎉 FULL RECURSIVE FEATURE EXTRACTION PIPELINE COMPLETE!")
    print("==================================================")


if __name__ == "__main__":
    main()
