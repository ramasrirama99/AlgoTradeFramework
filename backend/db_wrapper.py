import config
import pandas
import sqlite3 as sql


def get_ticker_data_between_dates(ticker, start_date, end_date, columns=[]):
    sql_query = '''SELECT * FROM historical_data WHERE ticker = "%s" AND timestamp
                   BETWEEN "%s" AND "%s"''' % (ticker, start_date, end_date)
    ticker_data = pandas.read_sql(sql_query, sql.connect(config.DB_NAME), parse_dates=['timestamp'])

    return ticker_data if len(columns) == 0 else ticker_data[columns]
