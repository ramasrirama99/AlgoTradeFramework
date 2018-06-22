CREATE TABLE IF NOT EXISTS tickers (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT
);

CREATE TABLE IF NOT EXISTS dates (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    date    TEXT
);


CREATE TABLE IF NOT EXISTS historical_data (
    date                INTEGER,
    ticker              INTEGER,
    open                REAL,
    high                REAL,
    low                 REAL,
    close               REAL,
    adjusted_close      REAL,
    volume              INTEGER,
    dividend_amount     REAL,
    split_coefficient   REAL,
    FOREIGN KEY(date) REFERENCES dates(id),
    FOREIGN KEY(ticker) REFERENCES tickers(id)
);
