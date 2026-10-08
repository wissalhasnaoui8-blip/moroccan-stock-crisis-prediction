"""ETL for French-language text data related to Moroccan markets and economy."""

from __future__ import annotations

import os
from datetime import datetime

import pandas as pd

START_DATE = "2016-01-01"
END_DATE = "2026-07-31"
OUTPUT_DIR = "data/raw/text"


def build_text_template() -> pd.DataFrame:
    columns = [
        "article_id",
        "date",
        "source_name",
        "source_type",
        "language",
        "title",
        "content",
        "url",
        "topic",
        "sentiment_score",
        "sentiment_label",
        "urgency_score",
        "is_market_related",
        "region",
    ]
    return pd.DataFrame(columns=columns)


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = build_text_template()
    out_path = os.path.join(OUTPUT_DIR, "text_articles_template.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved text template to {out_path}")


if __name__ == "__main__":
    main()
