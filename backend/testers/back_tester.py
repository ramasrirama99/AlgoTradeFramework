import psycopg2

import backend.db.db_wrapper as db
from backend.fileio import config

from datetime import datetime, timedelta, date

global time
global data


class Position:

    def __init__(self, order):
        self.ticker = order.ticker
        self.shares = order.shares
        self.init_equity = order.equity
        self.cur_equity = order.equity
        self.avg_quote = order.init_quote
        self.cur_quote = order.cur_quote
        self.shares = order.shares
        self.dividend = 0
        self.split = 1
        self.diff = 0

    def set_quote(self):
        historical_data = data.get_data(self.ticker, time.timestamp)
        if historical_data is not None:
            self.cur_quote = historical_data[4]

    def update(self):
        self.set_quote()
        # do some stuff with checking date and then split and dividend
        temp = self.cur_equity
        self.cur_equity = self.shares * self.cur_quote
        
        self.diff = self.cur_equity - temp

    def update_special(self):
        historical_data = data.get_data(self.ticker, time.timestamp)
        if historical_data is not None:
            self.dividend = historical_data[7]
            self.split = historical_data[8]
            self.shares *= self.split


class Portfolio:

    def __init__(self, name):
        self.name = name
        self.positions = {}
        self.orders = []
        self.history = []
        self.funds = 0
        self.diff = 0
        self.total_equity = 0

    def add_order_to_history(self, order):
        instance = HistoryInstance(ticker=order.ticker,
                                   buy=order.buy,
                                   limit=order.limit,
                                   shares=order.shares,
                                   equity=order.equity,
                                   cur_quote=order.cur_quote,
                                   time_placed=order.time_placed,
                                   time_expire=order.time_expire,
                                   time_exchanged=order.time_exchanged)
        self.history.append(instance)

    def add_dividend_to_history(self, position):
        instance = HistoryInstance(ticker=position.ticker,
                                   shares=position.shares,
                                   dividend=position.dividend,
                                   total_amount=position.shares*position.dividend,
                                   date=time.date)
        self.history.append(instance)

    def add_split_to_history(self, position):
        instance = HistoryInstance(ticker=position.ticker,
                                   shares=position.shares,
                                   split=position.split,
                                   cur_quote=position.cur_quote,
                                   date=time.date)
        self.history.append(instance)

    def add_order(self, order):
        ticker = order.ticker
        shares_valid = order.shares <= self.positions[ticker].shares
        if order.buy or (ticker in self.positions and shares_valid):
            self.orders.append(order)
            self.add_order_to_history(order)

    def expire(self, index, order):
        self.orders.pop(index)
        self.add_order_to_history(order)

    def calc_split(self, ticker):
        position = self.positions[ticker]
        position.shares *= position.split
        self.add_dividend_to_history(position)

    def calc_dividends(self, ticker):
        position = self.positions[ticker]
        payout = position.shares * position.dividend
        self.funds += payout
        self.add_split_to_history(position)

    def buy_position(self, index, order, position):
        self.orders.pop(index)
        self.funds -= position.cur_equity
        ticker = position.ticker

        if ticker in self.positions:
            pos = self.positions[ticker]
            weight1 = position.avg_quote * position.shares
            weight2 = pos.avg_quote * pos.shares
            total_shares = position.shares + pos.shares

            pos.shares = total_shares
            pos.avg_quote = (weight1 + weight2) / total_shares
            pos.init_equity = (weight1 + weight2)
        else:
            self.positions[ticker] = position

        self.add_order_to_history(order)

    def sell_position(self, index, order, position):
        ticker = position.ticker
        if ticker in self.positions:
            pos = self.positions[ticker]
            if position.shares <= pos.shares:
                self.orders.pop(index)
                self.funds += position.equity
                pos.shares -= position.shares
                if pos.shares == 0:
                    del self.positions[ticker]

        self.add_order_to_history(order)

    def deposit(self, funds):
        self.funds += funds
        self.total_equity += funds

    def withdraw(self, funds):
        if funds <= self.funds:
            self.funds -= funds
            self.total_equity -= funds

    def update(self):
        # iterate backwards for removing? otherwise compile list and remove all those elements
        for i, order in enumerate(self.orders):
            if time.timestamp > order.time_expire:
                self.expire(i, order)
            else:
                execute = order.update()
                if execute and order.buy:
                    position = Position(order)
                    self.buy_position(i, order, position)
                elif execute:
                    position = Position(order)
                    self.sell_position(i, order, position)
                self.orders.pop(i)
        for ticker, position in self.positions.items():
            position.update_special()
            self.calc_split(ticker)
            self.calc_dividends(ticker)

            position.update()
            self.total_equity += position.diff


class HistoryInstance:

    # ORDERS: ticker, buy, limit, time_placed, time_expire, limit_price, shares, time_exchanged, equity
    # DIVIDENDS: date, shares, per_share, total
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def message(self):
        for key, val in self.kwargs.items():
            message = '{key: <20} | {val: <20}\n'.format(key=key, val=val)
            print(message)


class Order:

    # Default market buy
    def __init__(self,
                 ticker,
                 time_placed,
                 time_expire,
                 buy=True,
                 limit=False,
                 limit_price=0,
                 shares=1):
        self.position = None
        self.ticker = ticker

        self.buy = buy
        self.limit = limit
        self.exchanged = False

        self.init_quote = 0
        self.cur_quote = 0
        self.limit_price = limit_price

        self.equity = 0
        self.shares = shares

        self.time_placed = time_placed
        self.time_expire = time_expire
        self.time_exchanged = None

    # Default market sell
    def __init__(self, position, time_expire, limit=False, limit_price=0):
        self.position = position
        self.ticker = position.ticker

        self.buy = False
        self.limit = limit
        self.exchanged = False

        self.init_quote = position.cur_quote
        self.cur_quote = position.cur_quote
        self.limit_price = limit_price

        self.equity = position.equity
        self.shares = position.shares

        self.time_placed = position.time_placed
        self.time_expire = time_expire
        self.time_exchanged = None

    def set_quote(self):
        historical_data = data.get_data(self.ticker, time.timestamp)
        if historical_data is not None:
            self.cur_quote = historical_data[4]

    def make_exchange(self):
        self.set_quote()

        if self.limit:
            if self.cur_quote <= self.limit_price:
                self.time_exchanged = time.timestamp
                self.init_quote = self.cur_quote
                self.equity = self.shares * self.init_quote
                self.exchanged = True
                return True
            else:
                return False
        else:
            self.time_exchanged = time.timestamp
            self.init_quote = self.cur_quote
            self.equity = self.shares * self.init_quote
            self.exchanged = True
            return True

    def update(self):
        # do some stuff with checking date and then split
        return self.make_exchange()


class TimeSimulator:

    def __init__(self, start_time):
        self.timestamp = start_time
        self.date = start_time.today()
        self.first = True

    # maybe skip day if time tick is not in data
    def time_tick(self, interval):
        self.timestamp += interval
        if self.timestamp.today() is not self.date:
            self.first = True
            self.date = self.timestamp.today()
        else:
            self.first = False


class HistoricalData:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='algotaf', user=config.USERNAME, password=config.PASSWORD, host=config.HOSTNAME)
        self.data = {}

    def populate_data(self,tickers):
        for ticker in tickers:
            self.data[ticker] = {}

            table_name = 'data_daily_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            for i in raw_data:
                self.data[ticker][i[0]] = i[1:]

            table_name = 'data_intraday_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            for i in raw_data:
                self.data[ticker][i[0]] = i[1:]

    def get_data(self, ticker, timestamp):
        if ticker in self.data and timestamp in self.data[ticker]:
            return self.data[ticker][timestamp]
        else:
            return None


def mock_decision_maker(portfolio, decision_list):

    if time.timestamp in decision_list:
        portfolio.add_order(decision_list[time.timestamp])


def populate_decision_list():
    timestamp1 = datetime(2019, 8, 6, 10, 30, 0)
    expiration1 = datetime(2019, 8, 6, 16, 0, 0)

    timestamp2 = datetime(2019, 8, 7, 12, 30, 0)
    expiration2 = datetime(2019, 8, 8, 16, 0, 0)

    timestamp3 = datetime(2019, 8, 13, 15, 0, 0)
    expiration3 = datetime(2019, 8, 13, 16, 0, 0)

    timestamp4 = datetime(2019, 8, 15, 12, 30, 0)
    expiration4 = datetime(2019, 8, 19, 16, 0, 0)

    # edge case invalid times
    timestamp5 = datetime(2019, 8, 19, 7, 30, 0)
    expiration5 = datetime(2019, 8, 19, 20, 0, 0)

    # edge case cancel
    timestamp6 = datetime(2019, 8, 23, 12, 0, 0)
    expiration6 = datetime(2019, 8, 23, 16, 0, 0)

    # edge case sell not enough shares
    timestamp7 = datetime(2019, 8, 23, 12, 1, 0)
    expiration7 = datetime(2019, 8, 23, 16, 0, 0)

    # edge case buy/sell 0
    timestamp8 = datetime(2019, 8, 23, 12, 2, 0)
    expiration8 = datetime(2019, 8, 23, 16, 0, 0)

    # edge case no funds
    timestamp9 = datetime(2019, 8, 23, 12, 3, 0)
    expiration9 = datetime(2019, 8, 23, 16, 0, 0)

    order1 = Order('aapl', timestamp1, expiration1, buy=True, limit=False, limit_price=0, shares=5)
    order2 = Order('msft', timestamp2, expiration2, buy=True, limit=True, limit_price=133.5, shares=5)
    order3 = Order('aapl', timestamp3, expiration3, buy=False, limit=False, limit_price=0, shares=1)
    order4 = Order('aapl', timestamp4, expiration4, buy=False, limit=True, limit_price=203, shares=4)
    order5 = Order('aapl', timestamp5, expiration5, buy=True, limit=False, limit_price=0, shares=5)
    order6 = Order('msft', timestamp6, expiration6, buy=True, limit=True, limit_price=130, shares=5)
    order7 = Order('msft', timestamp6, expiration6, buy=False, limit=True, limit_price=133.5, shares=20)
    order8 = Order('msft', timestamp6, expiration6, buy=True, limit=True, limit_price=133.5, shares=0)
    order9 = Order('msft', timestamp6, expiration6, buy=True, limit=True, limit_price=133.5, shares=100)

    return {timestamp1:order1, timestamp2:order2, timestamp3:order3, timestamp4:order4, timestamp5:order5, timestamp6:order6, timestamp7:order7, timestamp8:order8, timestamp9:order9}


def main():
    tickers = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo', 'bp', 'unh', 'cvs', 'tpr']
    data = HistoricalData()
    data.populate_data(tickers)
    timestamp = datetime(2019, 8, 11, 12, 30, 0)
    interval = timedelta(minutes=1)
    time = TimeSimulator(timestamp)
    folder = Portfolio('folder1')
    folder.deposit(9500)
    decision_list = populate_decision_list()
    
    while True:
        mock_decision_maker(folder, decision_list)
        folder.update()
        time.time_tick(interval)


if __name__ == '__main__':
    main()