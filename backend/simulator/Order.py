from backend.simulator.config import TIME, DATA


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
