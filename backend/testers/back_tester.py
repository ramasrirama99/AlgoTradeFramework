import psycopg2
from datetime import datetime, timedelta
from enum import Enum

import backend.db.db_wrapper as db
from backend.fileio import config
from other.benchmark import Benchmark

BENCH = Benchmark()


def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)


class HistoryType(Enum):
    PLACE_ORDER = 1
    EXCHANGE_ORDER = 2
    EXPIRE_ORDER = 3
    CANCEL_ORDER = 4
    DIVIDEND = 5
    SPLIT = 6


class Interval(Enum):
    MINUTE1 = 1
    MINUTE5 = 2
    MINUTE10 = 3
    MINUTE15 = 4
    MINUTE30 = 5
    HOUR = 6
    DAY = 7
    WEEK = 8
    MONTH = 9
    YEAR = 10
    ALL = 11


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
        self.dividend_date = None
        self.split_date = None

    def set_quote(self):
        quote = DATA.get_data(self.ticker, TIME.timestamp, 'close')
        if quote is not None:
            self.cur_quote = quote
            return True
        return False

    def update(self):
        if self.set_quote():
            temp = self.cur_equity
            self.cur_equity = self.shares * self.cur_quote
            self.diff = self.cur_equity - temp

    def update_special(self):
        dividend = DATA.get_data(self.ticker, TIME.date, 'dividend_amount')
        split = DATA.get_data(self.ticker, TIME.date, 'split_coefficient')
        if dividend is not None and split is not None:
            self.dividend = dividend
            self.split = split
        else:
            self.dividend = 0
            self.split = 1


class Portfolio:

    def __init__(self, name):
        self.name = name
        self.positions = {}
        self.orders = []
        self.history = {}
        self.funds = 0
        self.diff = 0
        self.total_equity = 0

    def add_order_to_history(self, history_type, message, order):
        instance = HistoryInstance(history_type,
                                   message=message,
                                   ticker=order.ticker,
                                   buy=order.buy,
                                   limit=order.limit,
                                   shares=order.shares,
                                   equity=round(order.equity, 2),
                                   cur_quote=order.cur_quote,
                                   time_placed=order.time_placed,
                                   time_expire=order.time_expire,
                                   time_exchanged=order.time_exchanged)
        instance.print_history()
        if order.ticker in self.history:
            if history_type in self.history[order.ticker]:
                self.history[order.ticker][history_type].append(instance)
            else:
                self.history[order.ticker][history_type] = [instance]
        else:
            self.history[order.ticker] = {history_type: [instance]}

    def add_dividend_to_history(self, position):
        instance = HistoryInstance(HistoryType.DIVIDEND,
                                   message='Dividend Paid',
                                   ticker=position.ticker,
                                   shares=position.shares,
                                   dividend=position.dividend,
                                   total_amount=round(position.shares*position.dividend, 2),
                                   date=TIME.date)
        instance.print_history()
        if position.ticker in self.history:
            if HistoryType.DIVIDEND in self.history[position.ticker]:
                self.history[position.ticker][HistoryType.DIVIDEND].append(instance)
            else:
                self.history[position.ticker][HistoryType.DIVIDEND] = [instance]
        else:
            self.history[position.ticker] = {HistoryType.DIVIDEND: [instance]}

    def add_split_to_history(self, position):
        instance = HistoryInstance(HistoryType.SPLIT,
                                   message='Stock Split',
                                   ticker=position.ticker,
                                   shares=position.shares,
                                   split=position.split,
                                   cur_quote=position.cur_quote,
                                   date=TIME.date)
        instance.print_history()
        if position.ticker in self.history:
            if HistoryType.SPLIT in self.history[position.ticker]:
                self.history[position.ticker][HistoryType.SPLIT].append(instance)
            else:
                self.history[position.ticker][HistoryType.SPLIT] = [instance]
        else:
            self.history[position.ticker] = {HistoryType.SPLIT: [instance]}

    def print_portfolio(self, interval):
        print('Portfolio - %s' % self.name)
        print('{key: <20} | {val: <20}'.format(key='funds', val=round(self.funds, 2)))
        print('{key: <20} | {val: <20}'.format(key='total_equity', val=round(self.total_equity, 2)))
        if len(self.positions) > 0:
            total_diff = 0
            total_percent = 0
            for ticker, position in self.positions.items():
                diff = 0
                if interval == Interval.ALL:
                    diff = position.cur_equity - position.init_equity
                percent = diff / position.cur_equity * 100
                total_diff += diff
                total_percent += percent

                print('{ticker: <20} | {diff: <20} | {percent}%'
                      .format(ticker=ticker, diff=round(diff, 2), percent=round(percent, 2)))

            total_percent /= len(self.positions)

            print('{key: <20} | {diff: <20} | {percent}%\n'
                  .format(key='total_diff', diff=round(total_diff, 2), percent=round(total_percent, 2)))

    def place_order(self, order):
        if order.shares > 0:
            ticker = order.ticker
            if order.buy or (ticker in self.positions and order.shares <= self.positions[ticker].shares):
                order.set_quote()
                if order.cur_quote * order.shares <= self.funds:
                    self.orders.append(order)
                    self.add_order_to_history(HistoryType.PLACE_ORDER, 'Order Placed', order)
                else:
                    print('Invalid order: Not enough funds\n')
            else:
                print('Invalid order: Not enough owned shares to sell\n')
        else:
            print('Invalid order: Shares must be > 0\n')

    def expire(self, index, order):
        self.orders.pop(index)
        self.add_order_to_history(HistoryType.EXPIRE_ORDER, 'Order Expired', order)

    def calc_split(self, ticker):
        position = self.positions[ticker]
        if position.split_date != TIME.date:
            position.split_date = TIME.date
            position.shares *= position.split
            if position.split > 1:
                self.add_split_to_history(position)

    def check_dividend_date(self, ticker):
        shares = 0
        if ticker in self.history and HistoryType.EXCHANGE_ORDER in self.history[ticker]:
            for instance in self.history[ticker][HistoryType.EXCHANGE_ORDER]:
                if instance.kwargs['buy']:
                    if TIME.date - timedelta(days=30) <= instance.kwargs['time_exchanged'].date():
                        shares += instance.kwargs['shares']
                else:
                    shares -= instance.kwargs['shares']
        return shares

    def get_exchange_dates(self, ticker):
        dates = {}
        if ticker in self.history and HistoryType.EXCHANGE_ORDER in self.history[ticker]:
            for instance in self.history[ticker][HistoryType.EXCHANGE_ORDER]:
                if TIME.date == instance.kwargs['time_exchanged'].date():
                    if instance.kwargs['buy']:
                        dates[instance.kwargs['time_exchanged']] = instance.kwargs['shares']
                    else:
                        dates[instance.kwargs['time_exchanged']] = instance.kwargs['shares'] * -1
        return dates

    def calc_dividends(self, ticker):
        position = self.positions[ticker]
        if position.dividend > 0 and position.dividend_date != TIME.date:
            shares = self.check_dividend_date(ticker)
            if shares > 0:
                position.dividend_date = TIME.date
                payout = position.shares * position.dividend
                self.funds += payout
                self.total_equity += payout
                self.add_dividend_to_history(position)

    def buy_position(self, index, order, position):
        self.orders.pop(index)
        self.funds -= position.shares * position.cur_quote
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

        self.add_order_to_history(HistoryType.EXCHANGE_ORDER, 'Order Exchanged', order)

    def sell_position(self, index, order, position):
        ticker = position.ticker
        if ticker in self.positions:
            pos = self.positions[ticker]
            if position.shares <= pos.shares:
                self.orders.pop(index)
                self.funds += position.shares * position.cur_quote
                pos.shares -= position.shares
                if pos.shares == 0:
                    del self.positions[ticker]

        self.add_order_to_history(HistoryType.EXCHANGE_ORDER, 'Order Exchanged', order)

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
            if TIME.timestamp > order.time_expire:
                self.expire(i, order)
            else:
                execute = order.update()
                if execute and order.buy:
                    position = Position(order)
                    self.buy_position(i, order, position)

                elif execute:
                    position = Position(order)
                    self.sell_position(i, order, position)
        self.total_equity = self.funds
        for ticker, position in self.positions.items():
            position.update_special()
            self.calc_split(ticker)
            self.calc_dividends(ticker)

            position.update()
            self.total_equity += position.cur_equity


class HistoryInstance:

    # ORDERS: ticker, buy, limit, time_placed, time_expire, limit_price, shares, time_exchanged, equity
    # DIVIDENDS: date, shares, per_share, total
    def __init__(self, history_type, message='', **kwargs):
        self.message = message
        self.history_type = history_type
        self.kwargs = kwargs

    def print_history(self):
        print(self.message)
        for key, val in self.kwargs.items():
            history = '{key: <20} | {val: <20}'.format(key=key, val=xstr(val))
            print(history)
        print()


class Order:

    # Default market buy
    def __init__(self,
                 ticker,
                 time_placed,
                 time_expire,
                 buy=True,
                 limit=False,
                 limit_price=0.0,
                 shares=1):

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

    def set_quote(self):
        quote = DATA.get_data(self.ticker, TIME.timestamp, 'close')
        if quote is not None:
            self.cur_quote = quote
            return True
        return False

    def make_exchange(self):
        if self.set_quote():
            if self.limit:
                limit_buy = self.buy and self.cur_quote <= self.limit_price
                limit_sell = not self.buy and self.cur_quote >= self.limit_price

                if limit_buy or limit_sell:
                    self.time_exchanged = TIME.timestamp
                    self.init_quote = self.cur_quote
                    self.equity = self.shares * self.init_quote
                    self.exchanged = True
                    return True
                else:
                    return False
            else:
                self.time_exchanged = TIME.timestamp
                self.init_quote = self.cur_quote
                self.equity = self.shares * self.init_quote
                self.exchanged = True
                return True
        return False

    def update(self):
        # do some stuff with checking date and then split
        return self.make_exchange()


class TimeSimulator:

    def __init__(self, start_time):
        self.timestamp = start_time
        self.date = start_time.date()
        self.first = True

    # maybe skip day if time tick is not in data
    def time_tick(self, interval):
        self.timestamp += interval
        if self.timestamp.date() != self.date:
            self.first = True
            self.date = self.timestamp.date()
        else:
            self.first = False


class HistoricalData:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='algotaf',
                                     user=config.USERNAME,
                                     password=config.PASSWORD,
                                     host=config.BACKUP_HOSTNAME)
        self.tickers = {}

    def populate_data(self, tickers):
        for ticker in tickers:
            self.tickers[ticker] = {}

            table_name = 'data_daily_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            columns = ('open',
                       'high',
                       'low',
                       'close',
                       'adjusted_close',
                       'volume',
                       'dividend_amount',
                       'split_coefficient')

            for row in raw_data:
                self.tickers[ticker][row[0]] = {}
                for i, col in enumerate(row[1:]):
                    self.tickers[ticker][row[0]][columns[i]] = col

            table_name = 'data_intraday_%s' % ticker
            raw_data = db.get_data_all(self.conn, table_name)
            columns = ('open',
                       'high',
                       'low',
                       'close',
                       'volume')
            for row in raw_data:
                self.tickers[ticker][row[0]] = {}
                for i, col in enumerate(row[1:]):
                    self.tickers[ticker][row[0]][columns[i]] = col

    def get_data(self, ticker, timestamp, attribute):
        if ticker in self.tickers and \
                timestamp in self.tickers[ticker] and \
                attribute in self.tickers[ticker][timestamp]:
            return self.tickers[ticker][timestamp][attribute]
        return None

    def get_diff(self, ticker, timestamp1, timestamp2, attribute1, attribute2):
        data1 = self.get_data(ticker, timestamp1, attribute1)
        data2 = self.get_data(ticker, timestamp2, attribute2)
        if data1 is not None and data2 is not None:
            return data2 - data1
        return 0


def mock_decision_maker(portfolio, decision_list):
    if TIME.timestamp in decision_list:
        for i in decision_list[TIME.timestamp]:
            portfolio.place_order(i)


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
    order7 = Order('msft', timestamp7, expiration7, buy=False, limit=True, limit_price=133.5, shares=20)
    order8 = Order('msft', timestamp8, expiration8, buy=True, limit=True, limit_price=133.5, shares=0)
    order9 = Order('msft', timestamp9, expiration9, buy=True, limit=True, limit_price=133.5, shares=100)
    order10 = Order('aapl', timestamp6, expiration6, buy=True, limit=False, limit_price=0, shares=5)

    return {timestamp1: [order1], timestamp2: [order2], timestamp3: [order3], timestamp4: [order4],
            timestamp5: [order5], timestamp6: [order6, order10], timestamp7: [order7], timestamp8: [order8],
            timestamp9: [order9]}


def main():
    print()
    tickers = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
               'bp', 'unh', 'cvs', 'tpr']
    global DATA
    global TIME
    global INTERVAL
    DATA = HistoricalData()
    DATA.populate_data(tickers)
    timestamp = datetime(2019, 8, 6, 0, 0, 0)
    INTERVAL = timedelta(minutes=1)
    TIME = TimeSimulator(timestamp)
    folder = Portfolio('folder1')
    folder.deposit(9500)
    decision_list = populate_decision_list()
    cur_date = TIME.date
    # BENCH.mark()
    print(cur_date)
    folder.print_portfolio(Interval.ALL)
    while TIME.timestamp <= datetime(2020, 8, 23, 20, 0, 0):
        mock_decision_maker(folder, decision_list)
        folder.update()
        TIME.time_tick(INTERVAL)

        if cur_date != TIME.date:
            print(cur_date)
            cur_date = TIME.date
            folder.print_portfolio(Interval.ALL)
            # BENCH.mark('One days time')
            # BENCH.mark()


if __name__ == '__main__':
    main()
