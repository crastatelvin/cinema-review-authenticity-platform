from langdetect import LangDetectException, detect


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        lower = text.lower()
        if any(token in lower for token in ["hai", "bahut", "paisa vasool", "bekaar"]):
            return "hi"
        return "en"


def multilingual_fake_adjustment(language: str) -> float:
    return 1.05 if language in {"hi", "hinglish"} else 1.0
