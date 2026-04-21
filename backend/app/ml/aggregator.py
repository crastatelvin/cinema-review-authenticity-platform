from __future__ import annotations

from statistics import mean

from app.ml.heuristics import sigmoid


WEIGHTS = [0.45, 0.2, 0.15, 0.1, 0.1]


def platform_score(f: float, d: float, b: float, m: float, t: float) -> float:
    x = WEIGHTS[0] * f + WEIGHTS[1] * d + WEIGHTS[2] * b + WEIGHTS[3] * m + WEIGHTS[4] * t
    return 1 - sigmoid(x * 4 - 1.2)


def final_authenticity_score(platform_scores: list[float]) -> float:
    if not platform_scores:
        return 0.0
    avg = mean(platform_scores)
    divergence = max(platform_scores) - min(platform_scores) if len(platform_scores) > 1 else 0.0
    return max(0.0, min(100.0, 100 * avg - (divergence * 10)))
