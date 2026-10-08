"""Build a merged multimodal dataset for crisis prediction."""

from __future__ import annotations

import os
from typing import Optional

import pandas as pd

START_DATE = "2016-01-01"
END_DATE = "2026-07-31"


def load_market_data(path: Optional[str] = None) -> pd.DataFrame:
    path = path or "data/raw/market/market_daily.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def load_text_data(path: Optional[str] = None) -> pd.DataFrame:
    path = path or "data/raw/text/text_articles_template.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def load_macro_data(path: Optional[str] = None) -> pd.DataFrame:
    path = path or "data/raw/macro/macro_indicators_template.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def build_dataset() -> pd.DataFrame:
    market = load_market_data()
    text = load_text_data()
    macro = load_macro_data()

    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
    merged = pd.DataFrame({"date": dates.strftime("%Y-%m-%d")})

    if not market.empty:
        market_daily = market.groupby("date", as_index=False).agg(
            market_index=("close_price", "mean"),
            market_return=("daily_return", "mean"),
            market_volatility=("rolling_volatility_20d", "mean"),
        )
        merged = merged.merge(market_daily, on="date", how="left")

    if not text.empty:
        text_daily = text.groupby("date", as_index=False).agg(
            sentiment_index=("sentiment_score", "mean"),
        )
        merged = merged.merge(text_daily, on="date", how="left")

    if not macro.empty:
        macro_daily = macro.groupby("date", as_index=False).agg(
            macro_index=("value", "mean"),
        )
        merged = merged.merge(macro_daily, on="date", how="left")

    merged["crisis_label"] = 0
    merged["crisis_window"] = 0

    return merged


def main() -> None:
    os.makedirs("data/processed", exist_ok=True)
    dataset = build_dataset()
    out_path = "data/processed/multimodal_daily_dataset.csv"
    dataset.to_csv(out_path, index=False)
    print(f"Saved merged dataset to {out_path}")


if __name__ == "__main__":
    main()
