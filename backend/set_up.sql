CREATE TABLE IF NOT EXISTS historical_data (
<<<<<<< HEAD
	[index]				INTEGER,
=======
    timestamp           TEXT,
>>>>>>> 8cd18be06e488c66bd5fe1b5c7112cf981e4cbf3
    ticker              TEXT,
    [timestamp]			TEXT,
    open                REAL,
    high                REAL,
    low                 REAL,
    close               REAL,
    adjusted_close      REAL,
    volume              INTEGER,
    dividend_amount     REAL,
    split_coefficient   REAL
);
