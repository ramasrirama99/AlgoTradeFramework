import yfinance as yf


def query(ticker, dates):
	stock = yf.Ticker(ticker)
	puts = []
	calls = []
	for i in dates:
		puts.append(stock.option_chain(i).puts)
		calls.append(stock.option_chain(i).calls)
	return puts, calls, stock.history(period='1d')['Close'][0]


def calculate(option, put_or_call, current_price, verbose=False):
	strikes = option['strike']
	volumes = {}
	asks = option['ask']
	if verbose:
		print('Current Price: {}'.format(current_price))
	if put_or_call:
		if verbose:
			print('PUT')
		# target_prices = [current_price * 0.9, current_price * 0.925, current_price * 0.95, current_price * 0.975]
		target_prices = [current_price * 0.95]
	else:
		if verbose:
			print('CALL')
		target_prices = [current_price * 1.025, current_price * 1.05, current_price * 1.075, current_price * 1.1]
		target_prices = [current_price * 1.05]
	if verbose:
		print('-----------------------------------------------------------------------------')
	growths = {}
	profits = {}
	initial = {}
	for target_price in target_prices:
		if verbose:
			print('Target Price: {}, Target Percent: {}'.format(target_price, target_price/current_price))
			print('-----------------------------------------------------------------------------')
		for i, val in enumerate(strikes):
			strike = strikes[i] * 100
			contract = asks[i] * 100
			if contract > 0:
				target = target_price * 100
				if put_or_call:
					profit = strike - contract - target
				else:
					profit = target - contract - strike
				growth = profit/contract

				if strike not in volumes:
					volumes[strike] = option['volume'][i]
				if profit < 0:
					profit = contract * -1
					growth = 0
				if strike not in growths:
					growths[strike] = growth
				else:
					growths[strike] += growth

				if strike not in profits:
					profits[strike] = profit
				else:
					profits[strike] += profit

				if strike not in initial:
					initial[strike] = contract
				else:
					initial[strike] = contract

				if verbose:
					print('strike: {:<10}| contract: {:<20}| profit: {:<20}| growth: {:<5}%'.format(strike, contract, profit, int(growth * 100)))
			else:
				profits[strike] = None
				initial[strike] = None

		if verbose:
			print('-----------------------------------------------------------------------------')

	return profits, initial


def profits(ticker, date, profit1, profit2, initial1, initial2):
	print(ticker)
	print(date)
	print()
	for key, val in profit1.items():
		if val is not None and key in profit2 and profit2[key] is not None:
			if key in profit2:
				val += profit2[key]
				val -= max(0.15 * initial1[key], 0.15 * initial2[key])
			if key in initial2:
				initial1[key] += initial2[key]
			print('strike: {:<10}|initial: {:<20}| profits: {:<5}'.format(key, initial1[key], val))
	print('-----------------------------------------------------------------------------')


def main():
	TICKER = 'BAC'
	DATES = ['2020-04-16', '2020-04-23', '2020-04-30', '2020-05-07', '2020-05-14']
	puts, calls, price = query(TICKER, DATES)
	print('Current Price: {}'.format(price))
	for i, val in enumerate(puts):	
		p1, i1 = calculate(puts[i], True, price)
		c1, i2 = calculate(calls[i], False, price)
		profits(TICKER, DATES[i], p1, c1, i1, i2)

if __name__ == '__main__':
	main()