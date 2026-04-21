from __future__ import annotations

from collections import Counter


def duplicate_fraction(texts: list[str]) -> float:
    if not texts:
        return 0.0
    normalized = [" ".join(t.lower().split()) for t in texts]
    counts = Counter(normalized)
    dup = sum(v for v in counts.values() if v > 1)
    return dup / len(texts)
