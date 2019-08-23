import psycopg2

from pgcopy import CopyManager
from pprint import pprint
from psycopg2.sql import SQL, Identifier, Literal
from time import sleep

import api_interactor as api
import config


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
    print('{message: <20}: Cached!'.format(message=table_name))


def store_data_daily(conn, ticker_list, calls_per_minute):
    cur = conn.cursor()
    columns = ('timestamp', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount',
               'split_coefficient')

    for ticker in ticker_list:
        table_name = 'data_daily_' + ticker.lower()

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp date, open float(8), high float(8), low float(8), \
            close float(8), adjusted_close float(8), volume float(8), dividend_amount float(8), \
            split_coefficient float(8));')

        if calls_per_minute >= 5:
            sleep(60)
            calls_per_minute = 0
        else:
            data_daily = api.get_daily_adjusted(ticker, outputsize='full')
            calls_per_minute += 1
        store_data(conn, cur, ticker, columns, table_name, query, data_daily)

    cur.close()


def store_data_intraday(conn, ticker_list, calls_per_minute):
    cur = conn.cursor()
    columns = ('timestamp', 'open', 'high', 'low', 'close', 'volume')

    for ticker in ticker_list:
        table_name = 'data_intraday_' + ticker.lower()

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp timestamp, open float(8), high float(8), low float(8), '
            'close float(8), volume float(8));')

        if calls_per_minute >= 5:
            sleep(60)
            calls_per_minute = 0
        else:
            data_intraday = api.get_intraday(ticker, outputsize='full')
            calls_per_minute += 1
        store_data(conn, cur, ticker, columns, table_name, query, data_intraday)

    cur.close()


def main():
    conn = psycopg2.connect(dbname='algotaf', user=config.USERNAME, password=config.PASSWORD, host=config.HOSTNAME)

    # ticker_list = config.TICKERS
    ticker_list = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'rht', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo', 'bp', 'unh', 'cvs', 'tpr']
    crypto_list = ['BTC', 'LTC', 'ETH']

    calls_per_minute = 0

    store_data_intraday(conn, ticker_list, calls_per_minute)
    store_data_daily(conn, ticker_list, calls_per_minute)


if __name__ == '__main__':
    main()