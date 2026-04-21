from __future__ import annotations

import pandas as pd


def load_deceptive_opinion_spam(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_yelpchi(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_amazon_fake(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
