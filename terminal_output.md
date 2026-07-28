# Terminal Execution Output

```powershell
PS E:\StressProject\MultimodalStressDetection> .\.venv\Scripts\python.exe scripts/run_full_extraction_pipeline.py

============================================================
PIPELINE STEP: WESAD RESP Feature Extraction
============================================================
Extracting Stage 3 features for WESAD (resp)...
Processing WESAD Subjects: 100%|█████████████| 15/15 [04:51<00:00, 19.41s/subject, subject=S17, step=extracting 514 windows]

==================================================
STAGE 3 FEATURE EXTRACTION SUMMARY
==================================================
Extracted feature rows : 7692
Feature columns count : 23
Saved feature dataset to: E:\StressProject\MultimodalStressDetection\data\processed\features\wesad_resp_features.parquet     

============================================================
PIPELINE STEP: WESAD ECG Baseline Profiles
============================================================
Building Stage 4 baseline profiles for 15 subjects...
==================================================
STAGE 4 BASELINE PROFILES SUMMARY
==================================================
Total profiles created  : 15
Valid profiles count   : 15 / 15
Saved baseline profiles to: E:\StressProject\MultimodalStressDetection\data\processed\baselines\wesad_ecg_profiles.parquet   

============================================================
PIPELINE STEP: WESAD ECG Baseline Anchoring
============================================================
==================================================
STAGE 5 FEATURE ANCHORING SUMMARY
==================================================
Total anchored rows : 7692
Total columns emitted: 77
Saved anchored dataset to: E:\StressProject\MultimodalStressDetection\data\processed\features\wesad_ecg_features_anchored.parquet

============================================================
PIPELINE STEP: StressID ECG Feature Extraction
============================================================
Extracting Stage 3 features for STRESSID (ecg)...
Processing StressID Subjects: 100%|██████████| 66/66 [00:09<00:00,  6.61subject/s, subject=y9z6, step=extracting 22 windows]

==================================================
STAGE 3 FEATURE EXTRACTION SUMMARY
==================================================
Extracted feature rows : 1412
Feature columns count : 35
Saved feature dataset to: E:\StressProject\MultimodalStressDetection\data\processed\features\stressid_ecg_features.parquet   

============================================================
PIPELINE STEP: StressID EDA Feature Extraction
============================================================
Extracting Stage 3 features for STRESSID (eda)...
Processing StressID Subjects: 100%|██████████| 66/66 [00:11<00:00,  5.84subject/s, subject=y9z6, step=extracting 22 windows]

==================================================
STAGE 3 FEATURE EXTRACTION SUMMARY
==================================================
Extracted feature rows : 1412
Feature columns count : 25
Saved feature dataset to: E:\StressProject\MultimodalStressDetection\data\processed\features\stressid_eda_features.parquet   

============================================================
PIPELINE STEP: StressID RESP Feature Extraction
============================================================
Extracting Stage 3 features for STRESSID (resp)...
Processing StressID Subjects: 100%|██████████| 66/66 [01:34<00:00,  1.44s/subject, subject=y9z6, step=extracting 22 windows]

==================================================
STAGE 3 FEATURE EXTRACTION SUMMARY
==================================================
Extracted feature rows : 1412
Feature columns count : 23
Saved feature dataset to: E:\StressProject\MultimodalStressDetection\data\processed\features\stressid_resp_features.parquet  

============================================================
PIPELINE STEP: StressID ECG Baseline Profiles
============================================================
Building Stage 4 baseline profiles for 65 subjects...
==================================================
STAGE 4 BASELINE PROFILES SUMMARY
==================================================
Total profiles created  : 65
Valid profiles count   : 63 / 65
Saved baseline profiles to: E:\StressProject\MultimodalStressDetection\data\processed\baselines\stressid_ecg_profiles.parquet

============================================================
PIPELINE STEP: StressID ECG Baseline Anchoring
============================================================
==================================================
STAGE 5 FEATURE ANCHORING SUMMARY
==================================================
Total anchored rows : 1412
Total columns emitted: 77
Saved anchored dataset to: E:\StressProject\MultimodalStressDetection\data\processed\features\stressid_ecg_features_anchored.parquet

============================================================
PIPELINE STEP: Automated Test Suite Verification (pytest)
============================================================
=================================================== test session starts ====================================================
platform win32 -- Python 3.12.7, pytest-8.2.2, pluggy-1.6.0
rootdir: E:\StressProject\MultimodalStressDetection
configfile: pyproject.toml
collected 6 items                                                                                                           

tests\test_pipeline.py ......                                                                                         [100%] 

==================================================== 6 passed in 0.31s ===================================================== 

============================================================
PIPELINE STEP: WESAD Step 4 LOSO Benchmark Evaluation Gate
============================================================
Loaded 7692 rows from E:\StressProject\MultimodalStressDetection\data\processed\features\wesad_ecg_features_anchored.parquet
Evaluating LOSO benchmark using 36 valid features across 15 subjects...

Executing Leave-One-Subject-Out (LOSO) Cross-Validation...

==================================================
PHYSIO LOSO BENCHMARK EVALUATION GATE
==================================================
LDA Model  -> Accuracy: 88.60%, F1: 0.7204
RF Model   -> Accuracy: 88.04%, F1: 0.7249
--------------------------------------------------
TARGET GATE BAND: 85.0% - 93.0% (Published Benchmark: 93.12% LDA, 92.01% RF)

[PASSED] Classification performance is strictly within expected WESAD benchmark range!

============================================================
PIPELINE STEP: StressID Physio LOSO Benchmark Evaluation Gate
============================================================
Loaded 1412 rows from E:\StressProject\MultimodalStressDetection\data\processed\features\stressid_ecg_features_anchored.parquet
Evaluating LOSO benchmark using 36 valid features across 65 subjects...

Executing Leave-One-Subject-Out (LOSO) Cross-Validation...

==================================================
PHYSIO LOSO BENCHMARK EVALUATION GATE
==================================================
LDA Model  -> Accuracy: 66.15%, F1: 0.3660
RF Model   -> Accuracy: 67.99%, F1: 0.4967
--------------------------------------------------
EXPECTED LOSO BAND: 65.0% - 72.0% (Published Non-LOSO Benchmark: 72.00% RF)

[PASSED] Classification performance is strictly within expected StressID LOSO range (0.65 - 0.72)!

==================================================
🎉 FULL RECURSIVE FEATURE EXTRACTION PIPELINE COMPLETE!
==================================================
PS E:\StressProject\MultimodalStressDetection> .\.venv\Scripts\python.exe scripts/eval_multimodal_fusion.py --dataset wesad
Evaluating Multimodal Late Decision Fusion for WESAD...
  Unimodal ECG   -> Accuracy: 88.04%, F1: 0.7249
  Unimodal EDA   -> Accuracy: 83.92%, F1: 0.6346
  Unimodal RESP  -> Accuracy: 85.71%, F1: 0.6679

==================================================
WESAD MULTIMODAL LATE DECISION FUSION RESULTS
==================================================
Average Rule Fusion -> Accuracy: 80.03%, F1: 0.4832
==================================================
PS E:\StressProject\MultimodalStressDetection> 
```
