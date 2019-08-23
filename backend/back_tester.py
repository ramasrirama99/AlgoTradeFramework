import api_interactor as api
import db_wrapper as db
import config

from datetime import datetime, timedelta

time = None

class Position:

    def __init__(self, order):
        self.ticker = order.ticker
        self.shares = order.shares
        self.init_equity = order.equity
        self.cur_equity = order.equity
        self.avg_quote = order.init_quote
        self.cur_quote = order.cur_quote
        self.shares = order.shares
        self.diff = 0


    def set_quote():
        data = get_data(ticker, time.timestamp)
        self.cur_quote = data[3]


    def update():
        set_quote()
        # do some stuff with checking date and then split and dividend
        temp = self.cur_equity
        self.cur_equity = self.shares * cur_quote
        
        self.diff = self.cur_equity - temp


    def dividend():


class Portfolio:

    def __init__(self, name):
        self.name = name
        self.positions = {}
        self.orders = []
        self.history = []
        self.funds = 0
        self.total_equity = funds

        # move elsewhere
        for key, val in positions.items():
            self.total_equity += val.cur_equity
            self.diff += val.diff


    def history_order(order):
        instance = History_Instance(ticker=order.ticker,
                                    buy=order.buy,
                                    limit=order.limit,
                                    shares=order.shares,
                                    equity=order.equity,
                                    cur_quote=order.cur_quote,
                                    time_placed=order.time_placed,
                                    time_expire=order.time_expire,
                                    time_exchanged=order.time_exchanged)
        self.history.append(instance)


    def add_order(order):
        ticker = order.ticker
        if order.buy or (not order.buy and ticker in positions and order.shares <= positions[ticker].shares):
            self.orders.append(order)
            history_order(order)


    def expire(order):
        history_order(order)
        orders.pop(index)


    def buy_position(index, order, position):
        self.orders.pop(index)
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

        history_order(order)


    def sell_position(index, order, position):
        ticker = position.ticker
        if ticker in self.positions:
            pos = self.positions[ticker]
            if position.shares <= pos.shares:
                self.orders.pop(index)
                self.funds += position.equity
                pos.shares -= position.shares
                if pos.shares == 0:
                    del positions[ticker]


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


    def update():
        # iterate backwards for removing? otherwise compile list and remove all those elements
        for i, order in enumerate(self.orders):
            if time.timestamp > i.time_expire:
                expire(i)
            else:
                execute = order.update()
                if execute and order.buy:
                    position = Position(order)
                    buy_position(i, order, position)
                elif execute:
                    position = Position(order)
                    sell_position(i, order, position)
                self.orders.pop(i)
        for i in self.positions:
            i.update()
            self.total_equity += i.diff


class History_Instance:

    # ORDERS: ticker, buy, limit, time_placed, time_expire, limit_price, shares, time_exchanged, equity
    # DIVIDENDS: date, shares, per_share, total
    def __init__(self, **kwargs):
        self.kwargs = kwargs


    def message():
        for key, val in self.kwargs.items():
            message = '{key: <20} | {val: <20}\n'.format(key=key, val=val)
            print(message)


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
                return True
            else:
                return False
        else:
            self.time_exchanged = time.timestamp
            self.init_quote = self.cur_quote
            self.equity = self.shares * self.init_quote
            self.exchanged = True
            return True


    def update():
        # do some stuff with checking date and then split
        return make_exchange()


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