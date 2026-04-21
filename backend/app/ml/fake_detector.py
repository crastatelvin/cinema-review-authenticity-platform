from __future__ import annotations

from functools import lru_cache

from transformers import pipeline


MODEL_ID = "martin-ha/toxic-comment-model"


@lru_cache(maxsize=2048)
def predict_fake_probability(text: str) -> float:
    # Practical baseline using transformer toxicity signal as a spam-manipulation proxy.
    # Replace MODEL_ID with your fine-tuned deceptive-review classifier artifact when available.
    classifier = _classifier()
    result = classifier(text[:512])[0]
    if result["label"].lower() in {"toxic", "label_1"}:
        return float(result["score"])
    return float(1 - result["score"])


@lru_cache(maxsize=1)
def _classifier():
    return pipeline("text-classification", model=MODEL_ID, truncation=True)
