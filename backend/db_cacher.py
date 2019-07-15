import psycopg2

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from pgcopy import CopyManager
from pprint import pprint
from psycopg2.sql import SQL, Identifier, Literal

import api_interactor as api
import config
from fileio import apikey


def verify_columns(api_cols, db_cols):
    for i, val in enumerate(api_cols):
        if val != db_cols[i]:
            raise Exception('Alpha Vantage API columns and database columns mismatch. API: \'%s\' and DB: \'%s\''
                            % (val, db_cols[i]))


def delete_duplicates(cur, table_name):
    cur.execute(SQL('DELETE FROM {} WHERE ctid NOT IN(SELECT MAX(ctid) FROM {} t GROUP BY t.timestamp);')
        .format(Identifier(table_name), Identifier(table_name)))


def store_data(conn, cur, ticker, columns, table_name, query, data):
    cur.execute(query.format(Identifier(table_name)))
    mgr = CopyManager(conn, table_name, columns)

    api_cols = data[0]
    verify_columns(api_cols, columns)

    raw_data = data[1:]
    mgr.copy(raw_data)
    delete_duplicates(cur, table_name)
    conn.commit()

    print("%s: Cached!" % ticker)


def store_data_daily(conn, ticker_list):
    cur = conn.cursor()
    columns = ('timestamp', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount',
               'split_coefficient')

    for ticker in ticker_list:
        table_name = 'data_daily_' + ticker.lower()

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp date, open float(8), high float(8), low float(8), \
            close float(8), adjusted_close float(8), volume float(8), dividend_amount float(8), \
            split_coefficient float(8));')

        data_daily = api.get_daily_adjusted(ticker, outputsize='full')
        store_data(conn, cur, ticker, columns, table_name, query, data_daily)

    cur.close()


def store_data_intraday(conn, ticker_list):
    cur = conn.cursor()
    columns = ('timestamp', 'open', 'high', 'low', 'close', 'volume')

    for ticker in ticker_list:
        table_name = 'data_intraday_' + ticker.lower()

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp datetime, open float(8), high float(8), low float(8), '
            'close float(8), volume float(8));').format(Identifier(table_name))

        data_intraday = api.get_intraday(ticker, outputsize='full')
        store_data(conn, cur, ticker, columns, table_name, query, data_intraday)

    cur.close()


def main():
    conn = psycopg2.connect(dbname='algotaf', user=config.USERNAME, password=config.PASSWORD, host=config.HOSTNAME)

    # ticker_list = config.TICKERS
    ticker_list = ['AAPL', 'AMZN', 'MSFT']
    crypto_list = ['BTC', 'LTC', 'ETH']

    store_data_daily(conn, ticker_list)


if __name__ == '__main__':
    main()