CREATE TABLE IF NOT EXISTS historical_data_daily (
    daily_id SERIAL,
    ticker TEXT,
    date TIMESTAMP,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    adjusted_close REAL,
    volume INTEGER,
    dividend_amount REAL,
    split_coefficient REAL
);
