from datetime import timedelta
from enum import Enum

from backend.simulator.Position import Position
from backend.simulator.config import TIME


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
