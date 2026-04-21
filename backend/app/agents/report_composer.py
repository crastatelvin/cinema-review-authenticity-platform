def compose_report(payload: dict) -> str:
    score = payload.get("authenticity_score", 0)
    if score >= 75:
        verdict = "mostly genuine"
    elif score >= 50:
        verdict = "mixed authenticity"
    else:
        verdict = "high fake-review risk"
    return (
        f"Final verdict: {verdict}. "
        f"Authenticity score: {score:.1f}/100. "
        "Check platform breakdown and flagged patterns for details."
    )
