import api_interactor as api
import db_wrapper as db
import config

from datetime import datetime, timedelta


class Position:

    def __init__(self, order):
        self.ticker = order.ticker
        self.shares = order.shares
        self.time = order.time
        self.time_placed = order.time_placed
        self.time_exchanged = order.time_exchanged
        self.init_equity = order.equity
        self.cur_equity = order.equity
        self.buy_quote = order.buy_quote
        self.cur_quote = order.cur_quote

    def update(interval, daily=True):


    def place_buy_order():
        if self.limit:

        else:


    def 


class Portfolio:

    def __init__(self, name, positions=[], funds=0, orders=[]):
        self.name = name
        self.positions = positions
        self.funds = funds
        self.orders = orders
    def add_position(position):
        self.funds -= position.cost
        self.positions.append(position)

    def update(interval, daily=True):
        for i in orders:
            orders.update()
        for i in positions:
            positions.update()



class Order:

    # Default market buy
    def __init__(self, conn, ticker, time, time_placed, time_expire, buy_sell = True, limit=False, limit_price=0, shares=1):
        self.conn = conn
        self.time = time
        self.ticker = ticker

        self.buy_sell = buy_sell
        self.limit = limit
        self.exchanged = False

        self.init_quote = 0
        self.cur_quote = 0
        self.equity = 0
        self.shares = shares
        self.limit_price = limit_price

        self.time_placed = time_placed
        self.time_expire = time_expire
        self.time_exchanged = None

    def set_quote():
        data = get_data(ticker, time.timestamp)
        cur_quote = data[3]

    def make_exchange(daily=True):
        set_quote(daily)
        if limit:
            if self.cur_quote <= limit_price:
                self.time_exchanged = time.timestamp
                self.init_quote = self.cur_quote
                self.equity = self.shares * self.init_quote
                self.exchanged = True
                return convert_to_position()
        else:
            self.time_exchanged = time.timestamp
            self.init_quote = self.cur_quote
            self.equity = self.shares * self.init_quote
            self.exchanged = True
            return convert_to_position()
        return None

    def update(interval, daily=True):
        time.time_tick(interval)
        return make_exchange(daily)

    def convert_to_position():
        return Position(self)


class TimeSimulator:

    def __init__(self, start_time):
        self.timestamp = start_time

    def time_tick(interval):
        timestamp += interval


class HistoricalData:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='algotaf', user=config.USERNAME, password=config.PASSWORD, host=config.HOSTNAME)
        self.data = {}

    def populate_data(tickers, daily=True):
        for ticker in tickers:
            if daily:
                table_name = 'data_daily_%s' % ticker
            else:
                table_name = 'data_intraday_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            data[ticker] = {}
            for i in raw_data:
                data[ticker][i[0]] = i[1:]

    def get_data(ticker, timestamp):
        return self.data[ticker][timestamp]


def main():
    data = HistoricalData()
    tickers = ['AAPL', 'AMZN', 'MSFT', 'AMD', 'NVDA', 'RHT', 'BABA', 'FITB', 'MU', 'FB', 'SQ', 'TSM', 'QCOM', 'MO', 'BP', 'UNH', 'CVS', 'TPR']
    data.populate_data()
    timestamp = datetime(2019, 7, 11, 12,  30, 0)
    interval = timedelta(minutes=1)
    time = TimeSimulator(timestamp)



    time.time_tick(interval)


if __name__ == '__main__':
    main()