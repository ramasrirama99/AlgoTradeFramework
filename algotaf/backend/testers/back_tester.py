from datetime import datetime, timedelta, time
from algotaf.backend.simulator.config import TIME, INTERVAL, DATA
from algotaf.backend.simulator.Portfolio import Portfolio, Interval
from algotaf.backend.simulator.Order import Order
from algotaf.other.benchmark import Benchmark
from algotaf.backend.testers.environment import StrategyEnvironment
from algotaf.backend.db import db_wrapper
import matplotlib.pyplot as plt
import sys

BENCH = Benchmark()


def mock_decision_maker(portfolio, decision_list):
    """
    A mockup of the decision function that will be made in the decision maker class
    :param portfolio: Portfolio class
    :param decision_list: Dict {datetime: List of Orders}
    """

    if TIME.timestamp in decision_list:
        for i in decision_list[TIME.timestamp]:
            portfolio.place_order(i)

class TestStrategy():
    def __init__(self):
        self.populate_decision_list()
        self.interval = Interval.MINUTE1

    def set_up(self):
        pass

    def populate_decision_list(self):
        """
        A function to populate the decision maker mockup
        :return: Dict {datetime: List of Orders}
        """
    
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

        self.decision_list = {timestamp1: [order1], timestamp2: [order2], timestamp3: [order3], timestamp4: [order4],
            timestamp5: [order5], timestamp6: [order6, order10], timestamp7: [order7], timestamp8: [order8],
            timestamp9: [order9]}


    def get_orders(self):
        curr_time = self.env.get_time()
        orders = []
        if curr_time in self.decision_list:
            for i in self.decision_list[curr_time]:
                orders.append(i)

        return orders


class Backtester(StrategyEnvironment):
    def __init__(self, strategy, portfolio, start_time='first_date', end_time='today'):
        self.start_time = start_time
        self.end_time = end_time
        self.curr_time = start_time
        self.portfolio = portfolio
        self.strategy = strategy
        self.interval = self.strategy.interval
        self.strategy.env = self
        self.portfolio.env = self
        self.orders = []

        if not self.interval:
            print("Strategy must have interval attribute.")
            sys.exit(1)


    def run(self):
        self.strategy.set_up()
        while self.curr_time < self.end_time:
            self.tick()

    def time_is_valid(self):
        is_valid = True

        if self.curr_time.weekday() >= 5:
            self.curr_time += Interval.to_timedelta(Interval.MINUTE1)
            return False

        if self.curr_time.time() <= time(9, 30, 0) or self.curr_time.time() >= time(20, 0, 0):
            self.curr_time += Interval.to_timedelta(Interval.MINUTE1)
            return False

        return True

    def tick(self):
        if not self.time_is_valid():
            return

        self.portfolio.update()
        self.orders += self.strategy.get_orders()
        self.check_orders()
        for order in self.orders:
            if self.time_is_valid():
                if order.limit:
                    if order.ticker not in self.portfolio.positions:
                        print("Not in portfolio or priced yet")
                    else:
                        if order.limit_price <= self.portfolio.positions[order.ticker].cur_quote:
                            self.portfolio.add_position(order)

                else:
                    self.portfolio.add_position(order)

        self.curr_time += Interval.to_timedelta(self.interval)


    def get_quote(self, ticker, timestamp=None, daily=False):
        if timestamp is None:
            timestamp = self.curr_time

        if timestamp > self.curr_time:
            print('Request of future data\n')

        quote = {}
        quote['open'] = DATA.get_data(ticker, timestamp, 'open', daily)
        quote['high'] = DATA.get_data(ticker, timestamp, 'high', daily)
        quote['low'] = DATA.get_data(ticker, timestamp, 'low', daily)
        quote['close'] = DATA.get_data(ticker, timestamp, 'close', daily)
        quote['volume'] = DATA.get_data(ticker, timestamp, 'volume', daily)
        
        return quote


    def get_quote_interval(self, ticker, start_date, end_date, daily=True):
        quotes = []
        if daily:
            num_intervals = (end_date - start_date).days
            interval = Interval.DAY
        else:
            num_intervals = (end_date - start_date).minutes
            interval = Interval.MINUTE1

        time_range = [start_date + Interval.to_timedelta(interval)*x for x in range(num_intervals)]

        for time in time_range:
            quotes.append(self.get_quote(ticker, timestamp=time, daily=daily))

        return quotes


    def get_time(self):
        return self.curr_time

    def check_orders(self):
        orders = []
        for i in self.orders[:]:
            if i.time_expire:
                if i.time_expire > self.curr_time:
                    orders.append(i)
            else:
                orders.append(i)
        self.orders = orders


def main():
    # print()
    # folder = Portfolio('folder1')
    # folder.deposit(9500)
    # decision_list = populate_decision_list()
    # cur_date = TIME.date
    # # BENCH.mark()
    # print(cur_date)
    # folder.print_portfolio(Interval.ALL)
    # while TIME.timestamp <= datetime(2019, 8, 23, 20, 0, 0):
    #     mock_decision_maker(folder, decision_list)
    #     folder.update()
    #     TIME.time_tick(INTERVAL)

    #     if cur_date != TIME.date:
    #         print(cur_date)
    #         cur_date = TIME.date
    #         folder.print_portfolio(Interval.ALL)
    #         # BENCH.mark('One days time')
    #         # BENCH.mark()
    strat = TestStrategy()
    portfolio = Portfolio('test')
    env = Backtester(strat, portfolio, start_time=datetime(2019, 7, 6, 0, 0, 0), end_time=datetime(2019, 8, 23, 20, 0, 0))
    env.run()

    plt.scatter(portfolio.equity_times, portfolio.equity_history)
    plt.xlabel('timestamps')
    plt.ylabel('Portfolio equity')
    plt.title("TestStrategy")
    plt.show()
    # plt.savefig('results.png')


if __name__ == '__main__':
    main()
