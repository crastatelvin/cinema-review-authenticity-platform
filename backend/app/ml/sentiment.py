POSITIVE = {"great", "amazing", "excellent", "loved", "masterpiece"}
NEGATIVE = {"bad", "awful", "boring", "worst", "waste"}


def sentiment_score(text: str) -> float:
    words = {w.strip(".,!?").lower() for w in text.split()}
    pos = len(words.intersection(POSITIVE))
    neg = len(words.intersection(NEGATIVE))
    return max(-1.0, min(1.0, (pos - neg) / 3))


def rating_sentiment_mismatch(rating: float | None, sentiment: float) -> float:
    if rating is None:
        return 0.0
    normalized_rating = (rating - 5) / 5
    return abs(normalized_rating - sentiment)
