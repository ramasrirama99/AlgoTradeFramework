import config
import psycopg2


def get_symbol_data_between_dates(symbol, start_date, end_date):
    conn = psycopg2.connect(dbname='algotaf', user=config.USER, password=config.PASSWORD, host=config.HOSTNAME)
    cur = conn.cursor()

    cur.execute('''SELECT * FROM data_daily_aapl WHERE symbol = "%s" AND timestamp
                   BETWEEN "%s" AND "%s"''' % (symbol, start_date, end_date))

    data = cur.fetchall()
    print(data)

    cur.close()
    conn.close()

    return data

get_symbol_data_between_dates('ABT', '2018-07-14', '2019-06-13')
