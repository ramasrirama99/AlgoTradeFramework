from datetime import datetime
from algotaf.backend.simulator.config import TIME, INTERVAL
from algotaf.backend.simulator.Portfolio import Portfolio, Interval
from algotaf.backend.simulator.Order import Order
from algotaf.other.benchmark import Benchmark
from algotaf.backend.testers.tester import StrategyEnvironment

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


def populate_decision_list():
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

    return {timestamp1: [order1], timestamp2: [order2], timestamp3: [order3], timestamp4: [order4],
            timestamp5: [order5], timestamp6: [order6, order10], timestamp7: [order7], timestamp8: [order8],
            timestamp9: [order9]}


class Backtester(StrategyEnvironment):
    def __init__(self, strategy, portfolio, start_time='first_date', end_time='today'):
        self.start_time = start_time
        self.end_time = end_time
        self.curr_time = start_time

        if strategy is None:
            print("strategy is None\n")
        else:
            strategy.env = self
            portfolio.env = self

    def run(self):
        while curr_time < end_time:
            tick()

    def tick(self):
        portfolio.update(self.curr_time)
        orders, interval = strategy.get_orders()
        for order in orders:
            portfolio.add_position(order)

        if interval < ASAP:
            self.curr_time += interval.to_datetime()
        else:
            exit()

    def get_quote(self, ticker, timestamp=None):
        if timestamp is None:
            timestamp = self.curr_time

        quote = {}
        quote['open'] = DATA.get_data(self.ticker, timestamp, 'open')
        quote['high'] = DATA.get_data(self.ticker, timestamp, 'high')
        quote['low'] = DATA.get_data(self.ticker, timestamp, 'low')
        quote['close'] = DATA.get_data(self.ticker, timestamp, 'close')
        quote['volume'] = DATA.get_data(self.ticker, timestamp, 'volume')

        return quote


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
    env = Backtester(None, None)


if __name__ == '__main__':
    main()
