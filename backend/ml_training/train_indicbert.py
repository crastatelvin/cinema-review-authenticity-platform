from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from datasets import Dataset
from sklearn.metrics import f1_score, roc_auc_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)


MODEL_NAME = "ai4bharat/indic-bert"


@dataclass
class TrainConfig:
    train_csv: str
    valid_csv: str
    output_dir: str = "artifacts/indicbert_fake_review"
    text_col: str = "text"
    label_col: str = "label"


def _to_dataset(path: str, text_col: str, label_col: str) -> Dataset:
    import pandas as pd

    frame = pd.read_csv(path)
    frame = frame[[text_col, label_col]].dropna()
    frame[label_col] = frame[label_col].astype(int)
    return Dataset.from_pandas(frame)


def train_indicbert(config: TrainConfig) -> dict:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train_ds = _to_dataset(config.train_csv, config.text_col, config.label_col)
    valid_ds = _to_dataset(config.valid_csv, config.text_col, config.label_col)

    def preprocess(batch):
        return tokenizer(batch[config.text_col], truncation=True, padding="max_length", max_length=256)

    train_ds = train_ds.map(preprocess, batched=True)
    valid_ds = valid_ds.map(preprocess, batched=True)
    train_ds = train_ds.rename_column(config.label_col, "labels")
    valid_ds = valid_ds.rename_column(config.label_col, "labels")
    train_ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    valid_ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
        preds = probs.argmax(axis=1)
        return {"f1": f1_score(labels, preds), "roc_auc": roc_auc_score(labels, probs[:, 1])}

    args = TrainingArguments(
        output_dir=config.output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=12,
        per_device_eval_batch_size=12,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_steps=50,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=valid_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    Path(config.output_dir).mkdir(parents=True, exist_ok=True)
    trainer.save_model(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)
    return {
        "f1": float(metrics.get("eval_f1", 0.0)),
        "roc_auc": float(metrics.get("eval_roc_auc", 0.0)),
        "model_path": config.output_dir,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_csv", required=True)
    parser.add_argument("--valid_csv", required=True)
    parser.add_argument("--output_dir", default="artifacts/indicbert_fake_review")
    parser.add_argument("--text_col", default="text")
    parser.add_argument("--label_col", default="label")
    args = parser.parse_args()

    config = TrainConfig(
        train_csv=args.train_csv,
        valid_csv=args.valid_csv,
        output_dir=args.output_dir,
        text_col=args.text_col,
        label_col=args.label_col,
    )
    print(train_indicbert(config))
