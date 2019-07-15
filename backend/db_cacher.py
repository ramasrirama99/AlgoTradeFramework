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


def store_data_daily(conn, ticker_list):
    cur = conn.cursor()
    for ticker in ticker_list:
        table_name = 'data_daily_' + ticker.lower()
        columns = ('timestamp', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount',
                   'split_coefficient')

        cur.execute(SQL('CREATE TABLE IF NOT EXISTS {} (timestamp date, open float(8), high float(8), low float(8), '
                        'close float(8), adjusted_close float(8), volume float(8), dividend_amount float(8), '
                        'split_coefficient float(8));').format(Identifier(table_name)))

        mgr = CopyManager(conn, table_name, columns)
        data_daily = api.get_daily_adjusted(ticker, outputsize='full')
        api_cols = data_daily[0]
        verify_columns(api_cols, columns)

        raw_data = data_daily[1:]
        mgr.copy(raw_data)
        conn.commit()
        print("%s: Cached!" % ticker)


def store_data_intraday(conn, ticker_list):
    for ticker in ticker_list:
        columns = ['open', 'high', 'low', 'close', 'volume']
        mgr = CopyManager(conn, table_name, columns)
        data_daily = api.get_daily_adjusted(ticker, outputsize='full')
        mgr.copy(data_daily)
        conn.commit()


def main():
    with open('fileio/sensitive_data.txt') as sensitive:
        user = sensitive.readline().strip()
        password = sensitive.readline().strip()
    with open('fileio/db_host.txt') as host:
        hostname = host.readline().strip()

    conn = psycopg2.connect(dbname='algotaf', user=user, password=password, host=hostname)

    # ticker_list = config.TICKERS
    ticker_list = ['AAPL', 'AMZN', 'MSFT']
    crypto_list = ['BTC', 'LTC', 'ETH']

    store_data_daily(conn, ticker_list)


if __name__ == '__main__':
    main()