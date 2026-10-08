from __future__ import annotations

import csv
from datetime import date, timedelta

START = date(2016, 1, 1)
END = date(2026, 7, 31)
OUTPUT_PATH = "data/processed/multimodal_daily_dataset.csv"


def iter_dates(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "date",
        "market_index",
        "market_return",
        "market_volatility",
        "sentiment_index",
        "macro_index",
        "macro_factor_1",
        "macro_factor_2",
        "crisis_label",
        "crisis_window",
    ])

    for d in iter_dates(START, END):
        writer.writerow([
            d.isoformat(),
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            0,
            0,
        ])

print(f"Created starter dataset at {OUTPUT_PATH} for {START.isoformat()} to {END.isoformat()}")
