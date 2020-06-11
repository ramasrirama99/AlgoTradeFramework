CREATE TABLE IF NOT EXISTS historical_data (
    history_id INTEGER,
    date TIMESTAMP,
    ticker              TEXT,
    [timestamp]		TEXT,
    open                REAL,
    high                REAL,
    low                 REAL,
    close               REAL,
    adjusted_close      REAL,
    volume              INTEGER,
    dividend_amount     REAL,
    split_coefficient   REAL
);
