from datetime import datetime, timedelta
from algotaf.backend.simulator.HistoricalData import HistoricalData
from algotaf.backend.simulator.TimeSimulator import TimeSimulator


TICKERS_SHORT = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
                 'bp', 'unh', 'cvs', 'tpr']

DATA = HistoricalData()
DATA.populate_data(TICKERS_SHORT)
INTERVAL = timedelta(minutes=1)
DAY_INTERVAL = timedelta(days=1)
TIME = TimeSimulator(datetime(2019, 8, 6, 0, 0, 0))
