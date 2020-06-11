import psycopg2
import time
from pgcopy import CopyManager, Replace
from psycopg2.sql import SQL, Identifier
from time import sleep
from algotaf.backend.apis import api_interactor as api
from algotaf.backend import config
from algotaf.other.benchmark import Benchmark

BACKUP = False
BENCH = Benchmark()


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

    cur.execute(SQL('DELETE FROM {} WHERE ctid NOT IN(SELECT MAX(ctid) FROM {} t GROUP BY t.timestamp);')
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

    cur.execute(SQL('SELECT * FROM {} ORDER BY {}.timestamp ASC;')
                .format(Identifier(table_name), Identifier(table_name)))
    data = cur.fetchall()

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

    BENCH.mark('Create table if not exists')

    BENCH.mark('Initial table copy')

    mgr = CopyManager(conn, table_name, columns)

    api_cols = data[0]
    verify_columns(api_cols, columns)

    records = data[1:]
    mgr.copy(records)

    BENCH.mark('Initial table copy')

    BENCH.mark('Delete duplicates')

    delete_duplicates(cur, table_name)

    BENCH.mark('Delete duplicates')

    BENCH.mark('Order table')

    ordered_records = order_table(conn, cur, table_name, columns)

    BENCH.mark('Order table')

    BENCH.mark('Store backup table')

    if BACKUP:
        store_backup(backup_conn, table_name, columns, ordered_records, query)

    BENCH.mark('Store backup table')

    BENCH.mark('Commit connections')

    conn.commit()

    if BACKUP:
        backup_conn.commit()

    BENCH.mark('Commit connections')

    print('{message: <20}: Cached!\n'.format(message=table_name))


def store_data_daily(conn, backup_conn, ticker_list, calls_per_minute):
    """
    Stores daily data for each ticker
    :param conn: AWS psycopg2 connection
    :param backup_conn: Backup psycopg2 connection
    :param ticker_list: List of tickers for API calls
    :param calls_per_minute: Max limit API calls per minute
    """

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
    """
    Stores intraday data for each ticker
    :param conn: AWS psycopg2 connection
    :param backup_conn: Backup psycopg2 connection
    :param ticker_list: List of tickers for API calls
    :param calls_per_minute: Max limit API calls per minute
    """

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


def schedule_jobs(conn, backup_conn, ticker_list):
    for i in config.TIMES:
        schedule.every().monday.at(i).do(store_data_intraday, conn, backup_conn, ticker_list, 0)
        schedule.every().tuesday.at(i).do(store_data_intraday, conn, backup_conn, ticker_list, 0)
        schedule.every().wednesday.at(i).do(store_data_intraday, conn, backup_conn, ticker_list, 0)
        schedule.every().thursday.at(i).do(store_data_intraday, conn, backup_conn, ticker_list, 0)
        schedule.every().friday.at(i).do(store_data_intraday, conn, backup_conn, ticker_list, 0)

    schedule.every().monday.at('15:00').do(store_data_daily, conn, backup_conn, ticker_list, 0)
    schedule.every().tuesday.at('15:00').do(store_data_daily, conn, backup_conn, ticker_list, 0)
    schedule.every().wednesday.at('15:00').do(store_data_daily, conn, backup_conn, ticker_list, 0)
    schedule.every().thursday.at('15:00').do(store_data_daily, conn, backup_conn, ticker_list, 0)
    schedule.every().friday.at('15:00').do(store_data_daily, conn, backup_conn, ticker_list, 0)


def main():
    print()
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

    # schedule_jobs(conn, backup_conn, ticker_list)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    store_data_intraday(conn, backup_conn, ticker_list, calls_per_minute)
    store_data_daily(conn, backup_conn, ticker_list, calls_per_minute)


if __name__ == '__main__':
    main()
