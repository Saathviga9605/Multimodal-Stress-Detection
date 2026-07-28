import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score


class UnimodalPhysioClassifier:
    """
    Unimodal physiological classifier operating on decoupled parquet tables.
    Supports LDA and Random Forest with strict Leave-One-Subject-Out (LOSO) evaluation.
    """

    def __init__(self, model_type: str = "rf", n_estimators: int = 100):
        self.model_type = model_type
        self.n_estimators = n_estimators

    def fit_predict_loso(self, df: pd.DataFrame) -> dict:
        meta_cols = {
            "dataset", "subject_id", "task", "window_id", "t_start", "t_end",
            "modality", "label_binary", "label_source", "is_baseline",
            "extractor_version", "config_hash", "quality", "quality_reason"
        }
        all_feats = [c for c in df.columns if c not in meta_cols]
        valid_feats = [c for c in all_feats if df[c].isna().mean() < 0.05]

        df_valid = df.dropna(subset=["label_binary"]).copy()
        X = df_valid[valid_feats].fillna(0.0).values
        y = df_valid["label_binary"].values
        subjects = df_valid["subject_id"].values

        unique_subjs = np.unique(subjects)
        preds = np.zeros_like(y)
        probs = np.zeros((len(y), 2))

        for test_subj in unique_subjs:
            train_mask = (subjects != test_subj)
            test_mask = (subjects == test_subj)

            X_tr, y_tr = X[train_mask], y[train_mask]
            X_te = X[test_mask]

            if self.model_type == "lda":
                clf = LinearDiscriminantAnalysis()
            else:
                clf = RandomForestClassifier(n_estimators=self.n_estimators, random_state=42)

            clf.fit(X_tr, y_tr)
            preds[test_mask] = clf.predict(X_te)
            if hasattr(clf, "predict_proba"):
                probs[test_mask] = clf.predict_proba(X_te)

        acc = float(accuracy_score(y, preds))
        f1 = float(f1_score(y, preds))

        return {
            "accuracy": acc,
            "f1_score": f1,
            "predictions": preds,
            "probabilities": probs,
            "subject_ids": subjects,
            "features_used": valid_feats,
        }
