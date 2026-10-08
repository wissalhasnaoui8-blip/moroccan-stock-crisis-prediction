CREATE TABLE IF NOT EXISTS market_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    company_name TEXT,
    sector TEXT,
    market_cap REAL,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    adj_close REAL,
    volume INTEGER,
    daily_return REAL,
    rolling_volatility_20d REAL,
    drawdown REAL,
    is_index INTEGER DEFAULT 0,
    source TEXT,
    UNIQUE(date, exchange, symbol)
);

CREATE TABLE IF NOT EXISTS text_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id TEXT UNIQUE,
    date DATE NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT,
    language TEXT DEFAULT 'fr',
    title TEXT,
    content TEXT,
    url TEXT,
    topic TEXT,
    sentiment_score REAL,
    sentiment_label TEXT,
    urgency_score REAL,
    is_market_related INTEGER DEFAULT 0,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS macro_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    indicator_name TEXT NOT NULL,
    indicator_group TEXT,
    value REAL,
    unit TEXT,
    source TEXT,
    frequency TEXT,
    UNIQUE(date, indicator_name, source)
);

CREATE TABLE IF NOT EXISTS crisis_labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    crisis_label INTEGER NOT NULL,
    label_type TEXT,
    confidence REAL,
    notes TEXT,
    UNIQUE(date, label_type)
);

CREATE TABLE IF NOT EXISTS multimodal_daily_dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    market_index TEXT,
    market_return REAL,
    market_volatility REAL,
    sentiment_index REAL,
    macro_index REAL,
    macro_factor_1 REAL,
    macro_factor_2 REAL,
    crisis_label INTEGER,
    crisis_window INTEGER,
    UNIQUE(date)
);

CREATE INDEX IF NOT EXISTS idx_market_daily_date ON market_daily(date);
CREATE INDEX IF NOT EXISTS idx_market_daily_symbol ON market_daily(symbol);
CREATE INDEX IF NOT EXISTS idx_text_articles_date ON text_articles(date);
CREATE INDEX IF NOT EXISTS idx_macro_indicators_date ON macro_indicators(date);
CREATE INDEX IF NOT EXISTS idx_macro_indicators_name ON macro_indicators(indicator_name);
CREATE INDEX IF NOT EXISTS idx_crisis_labels_date ON crisis_labels(date);
