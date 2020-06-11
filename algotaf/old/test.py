import requests

API_URL = 'https://www.alphavantage.co/query'

parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'AAPL',
    'output': 'compact',
    'datatype': 'csv',
    'apikey': 'WI3BQ0LCU79Y3QTU'
}

# Required parameters : (1) function, (2) symbol, (5) apikey
# Optional parameters :  (3) outputsize, (4) datatype

response = requests.get(API_URL, params=parameters)
if response.status_code == 200:
    print(response.text)
