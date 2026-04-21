from app.agents.report_composer import compose_report


def chat_reply(message: str, analysis: dict | None = None) -> str:
    if analysis:
        base = compose_report(analysis)
        if "why" in message.lower() or "reason" in message.lower():
            details = analysis.get("platforms", [])
            return base + " Platform signals: " + ", ".join(
                f"{d['platform']}={d['score']:.1f}" for d in details
            )
        return base
    lowered = message.lower()
    if "compare" in lowered:
        return "Run analyze first with a movie query. Then ask me to compare platform-level authenticity differences."
    if "fake" in lowered or "real" in lowered:
        return "Provide a movie name or a review page URL. I will fetch cross-platform reviews and score authenticity."
    return "I can analyze reviews, compare sources, and explain suspicious review patterns."
