import psycopg2
from datetime import datetime
from psycopg2.sql import SQL, Identifier
from backend import config
from other.benchmark import Benchmark

BENCH = Benchmark()


def get_data_interval(conn, table_name, start_date, end_date):
    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {} WHERE timestamp BETWEEN %s AND %s;')
                .format(Identifier(table_name)), (start_date, end_date))

    data = cur.fetchall()
    cur.close()
    return data


def get_data_all(conn, table_name):
    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {};')
                .format(Identifier(table_name)))

    data = cur.fetchall()
    cur.close()
    return data


def get_data_timestamp(conn, table_name, timestamp):
    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {} WHERE timestamp = %s;')
                .format(Identifier(table_name)), (timestamp,))

    data = cur.fetchall()
    cur.close()
    return data


def main():
    conn = psycopg2.connect(dbname='algotaf',
                            user=config.USERNAME,
                            password=config.PASSWORD,
                            host=config.HOSTNAME)

    timestamp = datetime(2019, 7, 11)

    BENCH.mark()

    print(get_data_timestamp(conn, 'data_daily_aapl', timestamp))

    BENCH.mark('Single timestamp daily')

    timestamp = datetime(2019, 7, 11, 12,  30, 0)

    BENCH.mark()

    print(get_data_timestamp(conn, 'data_intraday_aapl', timestamp))

    BENCH.mark('Single timestamp intraday')

    timestamp1 = datetime(2019, 8, 10)
    timestamp2 = datetime(2019, 8, 20)

    BENCH.mark()

    print(get_data_interval(conn, 'data_daily_aapl', timestamp1, timestamp2)[0])

    BENCH.mark('Interval timestamp daily')

    BENCH.mark()

    print(get_data_all(conn, 'data_daily_aapl')[0])

    BENCH.mark('All data daily')


if __name__ == '__main__':
    main()
