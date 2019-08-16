import api_interactor as api
import db_wrapper as db
import config

from datetime import datetime, timedelta

time = None

class Position:

    def __init__(self, order):
        self.ticker = order.ticker
        self.shares = order.shares
        self.time_placed = order.time_placed
        self.time_exchanged = order.time_exchanged
        self.init_equity = order.equity
        self.cur_equity = order.equity
        self.avg_quote = order.init_quote
        self.cur_quote = order.cur_quote
        self.shares = order.shares
        self.diff = 0

    def set_quote():
        data = get_data(ticker, time.timestamp)
        self.cur_quote = data[3]

    def update(interval):
        set_quote()
        # do some stuff with checking date and then split and dividend
        temp = self.cur_equity
        self.cur_equity = self.shares * cur_quote
        
        self.diff = self.cur_equity - temp

    def dividend():


class Portfolio:

    def __init__(self, name, positions={}, funds=0, orders=[]):
        self.name = name
        self.positions = positions
        self.funds = funds
        self.orders = orders
        self.total_equity = funds
        self.history = []
        message = 'Created Portfolio %s\n' % name
        for key, val in enumerate(positions):
            self.total_equity += val.cur_equity
            self.diff += val.diff
            message += 'Position {ticker: <5} | {shares: <7} shares\n'.format(ticker=i.ticker, shares=i.shares)
        for i in orders:
            if i.limit:
                message += 'Order {ticker: <5} | {shares: <7} shares | {limit_price: < 7} limit price | {time_placed: < 20} | {time_expire: <20}\n'
                    .format(ticker=i.ticker, shares=i.shares, limit_price=i.limit_price, time_placed=i.time_placed, time_expire=i.time_expire)
            else:
                message += 'Order {ticker: <5} | {shares: <7} shares | market price | {time_placed: < 20} | {time_expire: <20}\n'
                    .format(ticker=i.ticker, shares=i.shares, time_placed=i.time_placed, time_expire=i.time_expire)

        self.history.append(History_Instance(message, positions, orders))


    def add_order(order):
        ticker = order.ticker
        if order.buy:
            self.orders.append(order)
            message = 'Order Buy Placed {ticker: <5} | {shares: <7} shares\n'.format(ticker=ticker, shares=order.shares)
            self.history.append(History_Instance(message, orders=order))
        elif ticker in positions and order.shares <= positions[ticker].shares:
            self.orders.append(order)
            message = 'Order Sell Placed {ticker: <5} | {shares: <7} shares\n'.format(ticker=ticker, shares=order.shares)
            self.history.append(History_Instance(message, orders=order))

    def buy_position(position):
        self.funds -= position.equity
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
        message = 'Position Buy {ticker: <5} | {shares: <7} shares\n'.format(ticker=ticker, shares=position.shares)
        self.history.append(History_Instance(message, positions=position))

    def sell_position(position):
        ticker = position.ticker
        if ticker in self.positions:
            pos = self.positions[ticker]
            if position.shares <= pos.shares:
                self.funds += position.equity
                pos.shares -= position.shares
                if pos.shares == 0:
                    positions.remove(ticker)

                message = 'Position Sell {ticker: <5} | {shares: <7} shares\n'.format(ticker=ticker, shares=position.shares)
                self.history.append(History_Instance(message, positions=position))

    def sell_position(index, shares):
        pos = self.positions[index]
        if shares >= pos.shares:
            self.funds += pos.cur_quote * shares
            pos.shares -= shares
        if pos.shares == 0:
            self.positions.pop(index)

    def deposit(funds):
        self.funds += funds
        self.total_equity += funds

    def withdraw(funds):
        if funds <= self.funds:
            self.funds -= funds
            self.total_equity -= funds

    def update(interval):
        # iterate backwards for removing? otherwise compile list and remove all those elements
        for i in self.orders:
            pos = i.update(interval)
            if pos is not None:
                if i.buy:
                    buy_position(pos)
                else:
                    sell_position(pos)
                self.orders.pop(i)


        for i in self.positions:
            i.update(interval)
            self.total_equity += i.diff


class History_Instance:

    def __init__(self, message, positions=[], orders=[]):
        self.positions = positions
        self.orders = orders
        self.message = message


class Order:

    # Default market buy
    def __init__(self, ticker, time_placed, time_expire, buy = True, limit=False, limit_price=0, shares=1):
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

    def set_quote():
        data = get_data(ticker, time.timestamp)
        self.cur_quote = data[3]

    def make_exchange():
        set_quote()

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

    def update(interval):
        # do some stuff with checking date and then split
        pos = make_exchange()
        return pos

    def convert_to_position():
        if self.position is not None:
            return self.position
        else:
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

    def populate_data(tickers):
        for ticker in tickers:
            data[ticker] = {}

            table_name = 'data_daily_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            for i in raw_data:
                data[ticker][i[0]] = i[1:]

            table_name = 'data_intraday_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            for i in raw_data:
                data[ticker][i[0]] = i[1:]

    def get_data(ticker, timestamp):
        return self.data[ticker][timestamp]


def main():
    data = HistoricalData()
    tickers = ['AAPL', 'AMZN', 'MSFT', 'AMD', 'NVDA', 'RHT', 'BABA', 'FITB', 'MU', 'FB', 'SQ', 'TSM', 'QCOM', 'MO', 'BP', 'UNH', 'CVS', 'TPR']
    data.populate_data(tickers)
    timestamp = datetime(2019, 7, 11, 12,  30, 0)
    interval = timedelta(minutes=1)
    time = TimeSimulator(timestamp)
    time_not_ended = True
    order_queue = {}
    
    while time_not_ended:
        # call decision function
        # update portfolio(s)

        time.time_tick(interval)


if __name__ == '__main__':
    main()