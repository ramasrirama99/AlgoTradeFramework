import psycopg2
import time
import requests
import sys
from datetime import datetime
from pgcopy import CopyManager, Replace
from psycopg2.sql import SQL, Identifier
from time import sleep
from algotaf.backend.apis import api_interactor as api
from algotaf.backend import config
from algotaf.other.benchmark import Benchmark
from algotaf.backend.db import db_wrapper

BACKUP = False
BENCH = Benchmark()


def break_tickers(ticker_list, last_ticker):
    for i, ticker in enumerate(ticker_list):
        if ticker == last_ticker:
            return ticker_list[i:]            
    return ticker_list

def verify_columns(api_cols, db_cols):
    """
    Checks if API columns match with DB columns and raises exception if mismatch
    :param api_cols: List of columns names from API call data
    :param db_cols: List of columns names to compare with
    """

    for i, val in enumerate(api_cols):
        if val != db_cols[i]:
            raise Exception('Alpha Vantage API columns and database columns mismatch. API: \'%s\' and DB: \'%s\''
                            % (val, db_cols[i]))



# Replace with distinct, order by first, then select distinct
def delete_duplicates(cur, table_name):
    """
    Deletes rows with duplicate timestamps
    :param cur: AWS psycopg2 cursor
    :param table_name: Table name
    """

    # cur.execute(SQL('DELETE FROM {} WHERE ctid NOT IN(SELECT MAX(ctid) FROM {} t GROUP BY t.timestamp);')
    #             .format(Identifier(table_name), Identifier(table_name)))

    cur.execute(SQL('DELETE FROM {} a USING(SELECT MIN(ctid) as ctid, timestamp FROM {} GROUP BY timestamp HAVING COUNT(*) > 1) b WHERE a.timestamp = b.timestamp AND a.ctid <> b.ctid;')
                .format(Identifier(table_name), Identifier(table_name)))


def order_table(conn, cur, table_name, columns):
    """
    Orders table by timestamp in ascending order
    :param conn: AWS psycopg2 connection
    :param cur: AWS psycopg2 cursor
    :param table_name: Table name
    :param columns: List of column names
    :return: List of tuples with ordered data
    """
    print('sorting')
    cur.execute(SQL('SELECT * FROM {} ORDER BY {}.timestamp ASC;')
                .format(Identifier(table_name), Identifier(table_name)))
    data = cur.fetchall()
    print('done sorting')
    with Replace(conn, table_name) as temp:
        mgr = CopyManager(conn, temp, columns)
        mgr.copy(data)

    return data


def store_backup(conn, table_name, columns, records, query):
    """
    Stores records in backup database
    :param conn: Backup psycopg2 connection
    :param table_name: Table name
    :param columns: List of column names
    :param records: Ordered table records
    :param query: Query string for creating table
    """

    cur = conn.cursor()
    cur.execute(query.format(Identifier(table_name)))

    with Replace(conn, table_name) as temp:
        mgr = CopyManager(conn, temp, columns)
        mgr.copy(records)

    cur.close()
    

def store_data(conn, cur, backup_conn, columns, table_name, query, data):
    """
    Stores records in AWS and backup database
    :param conn: AWS psycopg2 connection
    :param cur: AWS psycopg2 cursor
    :param backup_conn: Backup psycopg2 connection
    :param columns: List of column names
    :param table_name: Table name
    :param query: Query string for creating table
    :param data: Raw API data
    """

    BENCH.mark('Create table if not exists')

    cur.execute(query.format(Identifier(table_name)))

    cur.execute(SQL('CREATE INDEX IF NOT EXISTS {} ON {}(timestamp ASC);')
            .format(Identifier(table_name + '_timestamp'), Identifier(table_name)))

    BENCH.mark('Create table if not exists')

    BENCH.mark('Initial table copy')

    mgr = CopyManager(conn, table_name, columns)

    # api_cols = data[0]
    # verify_columns(api_cols, columns)

    # records = data[1:]
    records = data
    mgr.copy(records)

    BENCH.mark('Initial table copy')

    BENCH.mark('Delete duplicates')

    delete_duplicates(cur, table_name)

    BENCH.mark('Delete duplicates')

    # BENCH.mark('Order table')

    # ordered_records = order_table(conn, cur, table_name, columns)

    # BENCH.mark('Order table')

    BENCH.mark('Store backup table')

    if BACKUP:
        store_backup(backup_conn, table_name, columns, ordered_records, query)

    BENCH.mark('Store backup table')

    BENCH.mark('Commit connections')

    conn.commit()

    if BACKUP:
        backup_conn.commit()

    BENCH.mark('Commit connections')
    return


def store_data_daily(backup_conn, ticker_list):
    """
    Stores daily data for each ticker
    :param conn: AWS psycopg2 connection
    :param backup_conn: Backup psycopg2 connection
    :param ticker_list: List of tickers for API calls
    :param calls_per_minute: Max limit API calls per minute
    """
    conn = db_wrapper.connect()
    cur = conn.cursor()

    columns = ('timestamp', 'open', 'high', 'low', 'close', 'volume', 'dividend_amount', 'split_coefficient')

    for ticker in ticker_list:
        table_name = 'data_daily_' + ticker.lower().replace('.', 'dot')

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp date, open float(8), high float(8), low float(8), \
            close float(8), volume float(8), dividend_amount float(8), split_coefficient float(8));')

        success = False
        BENCH.mark('API Call')
        while not success:
            try:
                data_daily = api.get_daily(ticker, 'alpaca')
                data_dividend, data_splits = api.get_actions_alpaca(ticker)
                success = True
            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                print('API_ERROR: SLEEPING...')
                sleep(1)
        BENCH.mark('API Call')

        connected = False
        while not connected:
            try:
                store_data(conn, cur, backup_conn, columns, table_name, query, data_daily)
                connected = True
            except psycopg2.OperationalError:
                print('DB_ERROR: RECONNECTING...')
                sleep(1)
                conn = db_wrapper.connect()
                cur = conn.cursor()
        print('{message: <20}: Cached!\n'.format(message=table_name))

    conn.close()
    cur.close()
    return


def store_data_intraday(backup_conn, ticker_list):
    """
    Stores intraday data for each ticker
    :param conn: AWS psycopg2 connection
    :param backup_conn: Backup psycopg2 connection
    :param ticker_list: List of tickers for API calls
    :param calls_per_minute: Max limit API calls per minute
    """

    conn = db_wrapper.connect()
    cur = conn.cursor()

    columns = ('timestamp', 'open', 'high', 'low', 'close', 'volume')

    for ticker in ticker_list:
        table_name = 'data_intraday_' + ticker.lower().replace('.', 'dot')

        query = SQL('CREATE TABLE IF NOT EXISTS {} (timestamp timestamp, open float(8), high float(8), low float(8), \
            close float(8), volume float(8));')

        success = False
        BENCH.mark('API Call')
        while not success:
            try:
                data_intraday = api.get_intraday(ticker, 'alpaca')
                success = True
            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                print('API_ERROR: SLEEPING...')
                sleep(1)
        BENCH.mark('API Call')

        connected = False
        while not connected:
            try:
                store_data(conn, cur, backup_conn, columns, table_name, query, data_intraday)
                connected = True
            except psycopg2.OperationalError:
                print('DB_ERROR: RECONNECTING...')
                sleep(1)
                conn = db_wrapper.connect()
                cur = conn.cursor()
        print('{message: <20}: Cached!\n'.format(message=table_name))

    conn.close()
    cur.close()
    return


def main():
    print()
    index = int(sys.argv[1])
    market = sys.argv[2]

    if BACKUP:
        backup_conn = psycopg2.connect(dbname=config.DB_NAME,
                                       user=config.USERNAME,
                                       password=config.PASSWORD,
                                       host=config.BACKUP_HOSTNAME)
    else:
        backup_conn = None

    # ticker_list = config.ALL_TICKERS
    # ticker_list = ticker_list[ticker_list.index('CELH'):]
    if market.upper() == 'AMEX':
        ticker_list = config.AMEX[index]
        ticker_list = break_tickers(ticker_list, '')
        store_data_intraday(backup_conn, ticker_list)
        # store_data_daily(backup_conn, ticker_list)
    elif market.upper() == 'NASDAQ':
        ticker_list = config.NASDAQ[index]
        ticker_list = break_tickers(ticker_list, '')
        store_data_intraday(backup_conn, ticker_list)
        # store_data_daily(backup_conn, ticker_list)
    elif market.upper() == 'NYSE':
        ticker_list = config.NYSE[index]
        ticker_list = break_tickers(ticker_list, '')
        store_data_intraday(backup_conn, ticker_list)
        # store_data_daily(backup_conn, ticker_list)


if __name__ == '__main__':
    main()
