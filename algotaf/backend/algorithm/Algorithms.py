from datetime import datetime, timedelta
from algotaf.backend.simulator.config import TIME, DATA, INTERVAL, DAY_INTERVAL
from algotaf.backend.simulator.Portfolio import Portfolio, Interval, HistoryType
from algotaf.backend.simulator.Order import Order
from algotaf.other.benchmark import Benchmark



class Algorithm:
    """
    Algorithm class for storing algorithm strategies
    """

    def __init__(self, name, portfolio):
        """
        :param name: Name of Algorithm
        :param portfolio: Portfolio object
        """

        self.name = name
        self.portfolio = portfolio
        self.algorithms = {}

    def make_decision(self, name):
        """
        :param name:
        :return:
        """

        orders = self.algorithms[name]

        for key, order in orders.items():
            if key == HistoryType.PLACE_ORDER:
                self.portfolio.place_order(order)
            elif key == HistoryType.CANCEL_ORDER:
                self.portfolio.cancel_order(order)
