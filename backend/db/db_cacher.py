import psycopg2

from pgcopy import CopyManager, Replace
from pprint import pprint
from psycopg2.sql import SQL, Identifier, Literal
from time import sleep

import backend.apis.api_interactor as api
from backend.fileio import config
from other.benchmark import Benchmark

BACKUP = True
BENCH = Benchmark()


def verify_columns(api_cols, db_cols):
    for i, val in enumerate(api_cols):
        if val != db_cols[i]:
            raise Exception('Alpha Vantage API columns and database columns mismatch. API: \'%s\' and DB: \'%s\''
                            % (val, db_cols[i]))


def delete_duplicates(cur, table_name):
    cur.execute(SQL('DELETE FROM {} WHERE ctid NOT IN(SELECT MAX(ctid) FROM {} t GROUP BY t.timestamp);')
                .format(Identifier(table_name), Identifier(table_name)))


def order_table(conn, cur, table_name, columns):
    cur.execute(SQL('SELECT * FROM {} ORDER BY {}.timestamp ASC;')
                .format(Identifier(table_name), Identifier(table_name)))
    data = cur.fetchall()

    with Replace(conn, table_name) as temp:
        mgr = CopyManager(conn, temp, columns)
        mgr.copy(data)

    return data


def store_backup(conn, table_name, columns, records, query):
    cur = conn.cursor()
    cur.execute(query.format(Identifier(table_name)))

    with Replace(conn, table_name) as temp:
        mgr = CopyManager(conn, temp, columns)
        mgr.copy(records)

    cur.close()
    

def store_data(conn, cur, backup_conn, columns, table_name, query, data):
    BENCH.mark()

    cur.execute(query.format(Identifier(table_name)))

    BENCH.mark('Create table if not exists')

    BENCH.mark()

    mgr = CopyManager(conn, table_name, columns)

    api_cols = data[0]
    verify_columns(api_cols, columns)

    records = data[1:]
    mgr.copy(records)

    BENCH.mark('Initial table copy')

    BENCH.mark()

    delete_duplicates(cur, table_name)

    BENCH.mark('Delete duplicates')

    BENCH.mark()

    ordered_records = order_table(conn, cur, table_name, columns)

    BENCH.mark('Order table')

    BENCH.mark()

    if BACKUP:
        store_backup(backup_conn, table_name, columns, ordered_records, query)

    BENCH.mark('Store backup table')

    BENCH.mark()

    conn.commit()
    backup_conn.commit()

    BENCH.mark('Commit connections')

    print('{message: <20}: Cached!'.format(message=table_name))


def store_data_daily(conn, backup_conn, ticker_list, calls_per_minute):
    cur = conn.cursor()

    columns = ('timestamp', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount',
               'split_coefficient')

    for ticker in ticker_list:
        table_name = 'data_daily_' + ticker.lower()

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp date, open float(8), high float(8), low float(8), \
            close float(8), adjusted_close float(8), volume float(8), dividend_amount float(8), \
            split_coefficient float(8));')

        if calls_per_minute is 5 or calls_per_minute is 0:
            print('SLEEPING 60s, 5 API CALLS MAX')
            sleep(60)
            calls_per_minute = 0

        data_daily = api.get_daily_adjusted(ticker, outputsize='full')
        calls_per_minute += 1
        store_data(conn, cur, backup_conn, columns, table_name, query, data_daily)

    cur.close()


def store_data_intraday(conn, backup_conn, ticker_list, calls_per_minute):
    cur = conn.cursor()

    columns = ('timestamp', 'open', 'high', 'low', 'close', 'volume')

    for ticker in ticker_list:
        table_name = 'data_intraday_' + ticker.lower()

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp timestamp, open float(8), high float(8), low float(8), '
                    'close float(8), volume float(8));')

        if calls_per_minute is 5 or calls_per_minute is 0:
            print('SLEEPING 60s, 5 API CALLS MAX')
            sleep(60)
            calls_per_minute = 0

        data_intraday = api.get_intraday(ticker, outputsize='full')
        calls_per_minute += 1
        store_data(conn, cur, backup_conn, columns, table_name, query, data_intraday)

    cur.close()


def main():
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.USERNAME,
                            password=config.PASSWORD,
                            host=config.HOSTNAME)

    if BACKUP:
        backup_conn = psycopg2.connect(dbname=config.DB_NAME,
                                       user=config.USERNAME,
                                       password=config.PASSWORD,
                                       host=config.BACKUP_HOSTNAME)
    else:
        backup_conn = None

    # ticker_list = config.TICKERS
    ticker_list = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
                   'bp', 'unh', 'cvs', 'tpr']
    crypto_list = ['BTC', 'LTC', 'ETH']

    calls_per_minute = 0

    store_data_intraday(conn, backup_conn, ticker_list, calls_per_minute)
    store_data_daily(conn, backup_conn, ticker_list, calls_per_minute)


if __name__ == '__main__':
    main()