from app.ml.aggregator import final_authenticity_score, platform_score


def test_platform_score_bounds():
    s = platform_score(0.2, 0.1, 0.0, 0.1, 0.1)
    assert 0 <= s <= 1


def test_final_score_bounds():
    v = final_authenticity_score([0.2, 0.8])
    assert 0 <= v <= 100
