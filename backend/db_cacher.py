import sqlite3 as sql
import pandas as pd
import api_interactor
import config

def store_ticker_in_db(conn, ticker, outputsize='full'):
	ticker_data = api_interactor.get_historical_data_for_ticker(ticker, outputsize=outputsize)
	print(ticker)
	
	try:
		if '{' in ticker_data.columns:
			del ticker_data['{']
		ticker_data.to_sql("historical_data", connection, if_exists="append")
	except sql.OperationalError:
                print(ticker)
                print(ticker_data.iloc[0])
                print('failed')
                raise RuntimeError
		ticker_data.to_sql("historical_data", conn, if_exists="append")
	except sql.OperationalError:
		print('failed')


def main():
	conn = sql.connect('test.db')
	cur = conn.cursor()
	cur.execute('DELETE FROM historical_data')
	ticker_list = config.TICKERS

	for ticker in range(int(len(ticker_list) / 10)):
		store_ticker_in_db(conn, ticker_list[ticker])

	table = pd.read_sql_query('select * from historical_data;', conn)
	print(table)



if __name__ == '__main__': main()
