from __future__ import annotations

from collections import Counter
from datetime import datetime
from math import exp


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def template_repetition_rate(texts: list[str]) -> float:
    if not texts:
        return 0.0
    bins = Counter(" ".join(t.lower().split()[:6]) for t in texts if t.strip())
    repeated = sum(v for v in bins.values() if v > 1)
    return repeated / len(texts)


def burstiness_index(timestamps: list[datetime | None]) -> float:
    valid = sorted([t for t in timestamps if t is not None])
    if len(valid) < 3:
        return 0.0
    deltas = [(valid[i] - valid[i - 1]).total_seconds() for i in range(1, len(valid))]
    quick_bursts = sum(1 for d in deltas if d < 1800)
    return quick_bursts / len(deltas)
