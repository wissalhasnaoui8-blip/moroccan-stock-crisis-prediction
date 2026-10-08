"""ETL for macroeconomic indicators relevant to Morocco."""

from __future__ import annotations

import os
from datetime import datetime

import pandas as pd

START_DATE = "2016-01-01"
END_DATE = "2026-07-31"
OUTPUT_DIR = "data/raw/macro"


def build_macro_template() -> pd.DataFrame:
    """Create an empty macro structure with common Moroccan indicators."""
    indicator_names = [
        "inflation_rate",
        "policy_rate",
        "exchange_rate_mad_usd",
        "exchange_rate_mad_eur",
        "gdp_growth",
        "unemployment_rate",
        "public_debt_ratio",
        "industrial_production_index",
        "trade_balance",
        "foreign_reserves_usd",
    ]

    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="MS")
    rows = []
    for dt in dates:
        for name in indicator_names:
            rows.append({
                "date": dt.strftime("%Y-%m-%d"),
                "indicator_name": name,
                "indicator_group": "macro",
                "value": None,
                "unit": "",
                "source": "Bank Al-Maghrib / HCP / World Bank",
                "frequency": "monthly",
            })

    return pd.DataFrame(rows)


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = build_macro_template()
    out_path = os.path.join(OUTPUT_DIR, "macro_indicators_template.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved macro template to {out_path}")


if __name__ == "__main__":
    main()
