import sqlite3 as sql
import requests
from io import StringIO
import pandas
#import config

API_URL = 'https://www.alphavantage.co/query'

def single_csv(symbol, apikey, function = 'TIME_SERIES_DAILY_ADJUSTED', output = 'compact', datatype = 'csv'):
	parameters = {
		'function': function,
		'symbol': symbol,
		'output': output,
		'datatype': datatype,
		'apikey': apikey
	}

	response = requests.get(API_URL, params = parameters)
	if(response.status_code == 200):
		cols = pandas.read_csv(StringIO(response.text))
		cols.insert(0, 'Ticker', symbol)
		return cols
	else:
		raise RequestFailed("Status_code was not 200")

ticker = input("Input a ticker\n")

csv_file = single_csv(ticker, 'WI3BQ0LCU79Y3QTU')

print(csv_file)