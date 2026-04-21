from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, roc_auc_score
from transformers import pipeline


def evaluate_model(model_path: str, csv_path: str, text_col: str = "text", label_col: str = "label") -> dict:
    frame = pd.read_csv(csv_path).dropna(subset=[text_col, label_col])
    clf = pipeline("text-classification", model=model_path, truncation=True)
    probs = []
    preds = []
    labels = frame[label_col].astype(int).tolist()
    for text in frame[text_col].tolist():
        result = clf(text[:512])[0]
        score = float(result["score"])
        prob_one = score if result["label"].lower() in {"label_1", "toxic"} else 1 - score
        probs.append(prob_one)
        preds.append(1 if prob_one >= 0.5 else 0)
    return {"f1": float(f1_score(labels, preds)), "roc_auc": float(roc_auc_score(labels, probs))}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--eval_csv", required=True)
    parser.add_argument("--text_col", default="text")
    parser.add_argument("--label_col", default="label")
    args = parser.parse_args()
    print(evaluate_model(args.model_path, args.eval_csv, text_col=args.text_col, label_col=args.label_col))
