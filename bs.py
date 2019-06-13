import bs4 as bs
import pickle
import requests
import os
import pandas_datareader.data as web
import datetime as dt
import csv

'''def save_sensex_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/BSE_SENSEX')
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	table = soup.find('table', {'class': 'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[1].text.replace('.','-')
		tickers.append(ticker)

	with open("sensextickers.pickle","wb") as f:
		pickle.dump(tickers,f)
	print(tickers)

	return tickers

save_sensex_tickers()	
'''
# save sensex_tickers()
def convert_to_list():
	with open('ListOfScripsFull.csv', 'r') as f:
		reader = csv.reader(f)
		tickers = list(reader)

	with open("sensextickers.pickle","wb") as f:
		pickle.dump(tickers,f)

	return tickers



def get_data_from_av(reload_sensex=False):
	if reload_sensex:
		tickers = convert_to_list()
	else:
		with open("stickers.pickle", "rb") as f:
			tickers = pickle.load(f)

	if not os.path.exists('stocks_dfs'):
		os.makedirs('stocks_dfs')

	start = dt.datetime(2010, 1, 1)
	end = dt.datetime.now()
	for ticker in tickers:

		if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, 'av-daily', start, end, access_key='ZV3NL5EA4BW0OKYT')
			df.reset_index(inplace=True)
			df.set_index("Date", inplace=True)
			df = df.drop("Symbol", axis=1)
			df.to_csv('stocks_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))


get_data_from_av()
