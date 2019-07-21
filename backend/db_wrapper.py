import config
import psycopg2
from datetime import datetime
from psycopg2.sql import SQL, Identifier, Literal


def get_data_interval(conn, table_name, start_date, end_date):
    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {} WHERE timestamp BETWEEN %s AND %s;').format(Identifier(table_name)), (start_date, end_date))

    data = cur.fetchall()
    cur.close()
    return data


def get_data_all(conn, table_name):
    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {};').format(Identifier(table_name)))

    data = cur.fetchall()
    cur.close()
    return data


def get_data_timestamp(conn, table_name, timestamp):
    cur = conn.cursor()

    cur.execute(SQL('SELECT * FROM {} WHERE timestamp = %s;').format(Identifier(table_name)), (timestamp,))

    data = cur.fetchall()
    cur.close()
    return data

def main():
    conn = psycopg2.connect(dbname='algotaf', user=config.USERNAME, password=config.PASSWORD, host=config.HOSTNAME)
    timestamp = datetime(2019, 7, 11)
    print(get_data_timestamp(conn, 'data_daily_aapl', timestamp))
    timestamp = datetime(2019, 7, 11, 12,  30, 0)
    print(get_data_timestamp(conn, 'data_intraday_aapl', timestamp))

    # get_data_interval(conn, 'data_daily_aapl', '2018-07-14', '2019-06-13')


if __name__ == '__main__':
    main()