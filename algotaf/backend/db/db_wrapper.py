import psycopg2
import pandas as pd
from datetime import datetime
from psycopg2.sql import SQL, Identifier
from algotaf.backend import config
from algotaf.other.benchmark import Benchmark

BENCH = Benchmark()


def get_data_interval(conn, table_name, start_date, end_date, pandas=False):
    """
    Queries database for data between the intervals
    :param conn: Psycopg2 connection
    :param table_name: Table name
    :param start_date: Interval starting datetime
    :param end_date: Interval ending datetime
    :return: Records within interval
    """

    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {} WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp ASC;')
                .format(Identifier(table_name)), (start_date, end_date))

    data = cur.fetchall()
    cur.close()
    if pandas:
        data = pd.DataFrame.from_records(data, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'dividend', 'split'])
    return data


def get_data_all(conn, table_name, pandas=False):
    """
    Queries database for all data for a given table
    :param conn: Psycopg2 connection
    :param table_name: Table name
    :return: All table records
    """

    if pandas:
        data = pd.read_sql_query('SELECT * FROM {} ORDER BY timestamp ASC;'
                                    .format(Identifier(table_name)),
                                    conn)
    else:
        cur = conn.cursor()

        cur.execute(SQL('SELECT * FROM {};')
                    .format(Identifier(table_name)))

        data = cur.fetchall()
        cur.close()
    return data


def get_data_timestamp(conn, table_name, timestamp, pandas=False):
    """
    Queries database for single record at timestamp
    :param conn: Psycopg2 connection
    :param table_name: Table name
    :param timestamp: Datetime
    :return: Record at timestamp
    """

    if pandas:
        data = pd.read_sql_query('SELECT * FROM {} WHERE timestamp = %s;'
                                    .format(Identifier(table_name), (timestamp,)),
                                    conn)
    else:
        cur = conn.cursor()

        try:
            cur.execute(SQL('SELECT * FROM {} WHERE timestamp = %s;')
                    .format(Identifier(table_name)), (timestamp,))
        except Exception:
            return None
        data = cur.fetchall()
        cur.close()
    return data


def connect():
    """
    Connects to database
    :return: Psycopg2 connection
    """
    conn = psycopg2.connect(dbname=config.DB_NAME,
                        user=config.USERNAME,
                        password=config.PASSWORD,
                        host=config.HOSTNAME)
    return conn


def main():
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.USERNAME,
                            password=config.PASSWORD,
                            host=config.HOSTNAME)

    timestamp = datetime(2019, 7, 11)

    BENCH.mark('Single timestamp daily')

    print(get_data_timestamp(conn, 'data_daily_aapl', timestamp))

    BENCH.mark('Single timestamp daily')

    timestamp = datetime(2019, 7, 11, 12, 30, 0)

    BENCH.mark('Single timestamp intraday')

    print(get_data_timestamp(conn, 'data_intraday_aapl', timestamp))

    BENCH.mark('Single timestamp intraday')

    timestamp1 = datetime(2019, 8, 10)
    timestamp2 = datetime(2019, 8, 20)

    BENCH.mark('Interval timestamp daily')

    print(get_data_interval(conn, 'data_daily_aapl', timestamp1, timestamp2)[0])

    BENCH.mark('Interval timestamp daily')

    BENCH.mark('All data daily')

    print(get_data_all(conn, 'data_daily_aapl')[0])

    BENCH.mark('All data daily')


if __name__ == '__main__':
    main()
