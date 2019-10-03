from algotaf.backend.simulator.config import TIME, DATA


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
