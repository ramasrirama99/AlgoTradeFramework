from datetime import datetime, timedelta
from algotaf.backend.simulator.config import TIME, DATA, INTERVAL, DAY_INTERVAL
from algotaf.backend.simulator.Portfolio import Portfolio, Interval, HistoryType
from algotaf.backend.simulator.Order import Order
from algotaf.backend.algorithm import Algorithms
from algotaf.other.benchmark import Benchmark


def mean(series):
	"""
	"""

	avg = 0
	for i in series:
		avg += i
	avg /= len(series)
	return avg

class MovingAverage(Algorithms):
    """
    Algorithm class for storing algorithm strategies
    """

    def __init__(self, name, portfolio, shortterm, longterm):
        """
        :param name: Name of Algorithm
        """

        self.name = name
        self.portfolio = portfolio
        self.ma_short = {}
        self.ma_long = {}
		self.shortterm = shortterm
		self.longterm = longterm
		wl = self.portfolio.watch_list
		for ticker, val in wl.items():
			ma_short[ticker] = {}
			ma_long[ticker] = {}
			ma_short[ticker][TIME.timestamp] = mean(DATA.get_data_interval(ticker,
																   TIME.timestamp,
																   TIME.timestamp + timedelta(days=self.shortterm),
																   'close',
																   config.DAY_INTERVAL))
			ma_long[ticker][TIME.timestamp] = mean(DATA.get_data_interval(ticker,
																  TIME.timestamp,
																  TIME.timestamp + timedelta(days=self.longterm),
																  'close',
																  config.DAY_INTERVAL))



	def update(self):
		"""
		"""

		wl = self.portfolio.watch_list
		for ticker, val in wl.items():
			if ticker in ma_short and ticker in ma_long:
				ma_short[TIME.timestamp].append(mean(DATA.get_data_interval(ticker,
																	   TIME.timestamp,
																	   TIME.timestamp + timedelta(days=20),
																	   'close',
																	   config.DAY_INTERVAL)))
				ma_long[TIME.timestamp].append(mean(DATA.get_data_interval(ticker,
																	  TIME.timestamp,
																	  TIME.timestamp + timedelta(days=150),
																	  'close',
																	  config.DAY_INTERVAL)))
			else:
				ma_short[TIME.timestamp] = mean(DATA.get_data_interval(ticker,
																	   TIME.timestamp,
																	   TIME.timestamp + timedelta(days=20),
																	   'close',
																	   config.DAY_INTERVAL))
				ma_long[TIME.timestamp] = mean(DATA.get_data_interval(ticker,
																	  TIME.timestamp,
																	  TIME.timestamp + timedelta(days=150),
																	  'close',
																	  config.DAY_INTERVAL))