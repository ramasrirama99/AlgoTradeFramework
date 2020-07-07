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
		self.interval = Interval.DAY
		self.is_bought = False

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
			return []
		self.curr_date = curr_time.date()

		sma_short = self.get_sma(TEST_STOCK, self.short_period)
		sma_long = self.get_sma(TEST_STOCK, self.long_period)

		quote = self.env.get_quote(TEST_STOCK, daily=True)
		if quote['open'] is None:
			return []
		price = (quote['open'] + quote['close']) / 2
		
		if not self.is_bought and sma_short > sma_long:
			print(curr_time.date())
			print('short: ', sma_short)
			print('long: ', sma_long)
			self.is_bought = True
			self.num_shares = (self.env.get_portfolio().funds / price) / 2
			print('buy %d shares at %f' % (self.num_shares, price), '\n')
			return [Order(TEST_STOCK, curr_time, None, buy=True, limit=False, limit_price=0, shares=self.num_shares)]
		elif self.is_bought and sma_long > sma_short:
			print(curr_time.date())
			print('short: ', sma_short)
			print('long: ', sma_long)
			print('sell %d shares at %f' % (self.num_shares, price), '\n')
			self.is_bought = False
			return [Order(TEST_STOCK, curr_time, None, buy=False, limit=False, limit_price=0, shares=self.num_shares)]

		return []

def main():
    strat = CrossoverStrategy(short_period=40, long_period=200)
    portfolio = Portfolio('CrossoverStrategy')
    env = Backtester(strat, portfolio, start_time=datetime(2000, 6, 10, 0, 0, 0), end_time=datetime(2019, 8, 23, 20, 0, 0))
    env.run()

    plt.plot(portfolio.equity_times, portfolio.equity_history)
    plt.xlabel('timestamps')
    plt.ylabel('Portfolio equity')
    plt.show()
    plt.savefig('results.png')


if __name__ == '__main__':
    main()