"""ETL for Moroccan market data (daily OHLCV, indices, equities)."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Iterable

import pandas as pd
import yfinance as yf

START_DATE = "2016-01-01"
END_DATE = "2026-07-31"
OUTPUT_DIR = "data/raw/market"


def fetch_index_series(symbols: Iterable[str]) -> pd.DataFrame:
    """Fetch public market series from Yahoo Finance when available."""
    frames = []
    for symbol in symbols:
        try:
            df = yf.download(symbol, start=START_DATE, end=END_DATE, progress=False, auto_adjust=False)
            if df.empty:
                continue
            df = df.reset_index()
            df["symbol"] = symbol
            df["date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
            frames.append(df)
        except Exception as exc:
            print(f"Skipping {symbol}: {exc}")

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def compute_market_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.rename(columns={
        "Date": "date",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Adj Close": "adj_close",
        "Volume": "volume",
    })

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["daily_return"] = df.groupby("symbol")["close_price"].pct_change()
    df["rolling_volatility_20d"] = (
        df.groupby("symbol")["daily_return"]
        .transform(lambda s: s.rolling(20, min_periods=1).std())
    )
    df["drawdown"] = (
        df.groupby("symbol")["close_price"]
        .transform(lambda s: s / s.cummax() - 1)
    )
    df["exchange"] = "CASABLANCA"
    df["source"] = "yfinance"
    return df


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Add Moroccan symbols if public coverage is available.
    # For the Casablanca market, a production pipeline should use official exchange data or licensed feeds.
    symbols = [
        "^MASE.MI",
        "^MADEX.MI",
        "^MASI.MI",
    ]

    raw = fetch_index_series(symbols)
    cleaned = compute_market_features(raw)

    out_path = os.path.join(OUTPUT_DIR, "market_daily.csv")
    cleaned.to_csv(out_path, index=False)
    print(f"Saved market data to {out_path}")


if __name__ == "__main__":
    main()
