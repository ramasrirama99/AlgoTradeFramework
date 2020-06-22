from algotaf.backend.strategies.strategy import Strategy
from datetime import datetime, timedelta
from algotaf.backend.simulator.Portfolio import Portfolio, Interval
from algotaf.backend.simulator.Order import Order
from algotaf.backend.testers.back_tester import Backtester, TestStrategy
import numpy as np
import matplotlib.pyplot as plt


TICKERS_SHORT = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
                 'bp', 'unh', 'cvs', 'tpr']
TEST_STOCK = 'amzn'

class CrossoverStrategy(Strategy):
	def __init__(self, short_period=50, long_period=200):
		self.long_period = long_period
		self.short_period = short_period
		self.is_bought = False
		self.curr_date = None

	def set_up(self):
		self.curr_date = self.env.get_time().date()

	def get_sma(self, ticker, num_days):
		curr_time = self.env.get_time()
		quotes = self.env.get_quote_interval(TEST_STOCK, curr_time - timedelta(days=num_days), curr_time)
		closes = [quote['close'] for quote in quotes if quote['close'] != None]

		return np.mean(closes)

	def get_orders(self):
		curr_time = self.env.get_time()
		if self.curr_date == curr_time.date():
			return [], Interval.DAY

		sma_short = self.get_sma(TEST_STOCK, self.short_period)
		sma_long = self.get_sma(TEST_STOCK, self.long_period)
		# print(curr_time)
		# print('short - long: ', sma_short - sma_long)

		quote = self.env.get_quote(TEST_STOCK)
		price = (quote['open'] + quote['close']) / 2
		if not self.is_bought and sma_short > sma_long:
			print(curr_time.date())
			print('short: ', sma_short)
			print('long: ', sma_long)
			print('buy at: ', price, '\n')
			self.is_bought = True
			return [Order(TEST_STOCK, curr_time, None, buy=True, limit=False, limit_price=0, shares=10)], Interval.DAY
		elif self.is_bought and sma_long > sma_short:
			print(curr_time.date())
			print('short: ', sma_short)
			print('long: ', sma_long)
			print('sell at: ', price, '\n')
			self.is_bought = False
			return [Order(TEST_STOCK, curr_time, None, buy=False, limit=False, limit_price=0, shares=10)], Interval.DAY

		return [], Interval.DAY

def main():
    strat = CrossoverStrategy(short_period=75, long_period=400)
    portfolio = Portfolio('CrossoverStrategy')
    env = Backtester(strat, portfolio, start_time=datetime(2016, 7, 8, 0, 0, 0), end_time=datetime(2019, 8, 23, 20, 0, 0))
    env.run()

    plt.plot(portfolio.equity_times, portfolio.equity_history)
    plt.xlabel('timestamps')
    plt.ylabel('Portfolio equity')
    plt.show()
    plt.savefig('results.png')


if __name__ == '__main__':
    main()