import bs4 as bs
import pickle
import requests
import os
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import csv
import urllib.request, json
import pandas as pd

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
        scrips = list(reader)
    tickers = []
    for i in range(len(scrips)):

        tickers.append(scrips[i][1])

    del tickers[0]
    for ticker in tickers:
        ticker = ticker.replace('.','-').strip()
    tickers = ['BSE:'+ x for x in tickers]

    outfile = open("bsetickers.pickle","wb")
    pickle.dump(tickers,outfile)
    outfile.close()
    return tickers

#convert_to_list()
def get_data_from_av(reload_sensex=False):
    if reload_sensex:
        tickers = convert_to_list()
    else:
        with open("bsetickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stocks_dfs'):
        os.makedirs('stocks_dfs')

    start = dt.datetime(2019, 6, 12)
    end = dt.datetime.now()
    api_key = 'ZV3NL5EA4BW0OKYT'
    tick_names = [s.replace(':', '-') for s in tickers]
    

    for ticker in tickers:
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)
        file_to_save = 'stock_dfs/%s.csv'%ticker.replace(':','-')
        print(ticker)

        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data = json.loads(url.read().decode())
            # extract stock market data
            data = data['Time Series (Daily)']
            df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
            for k,v in data.items():
                date = dt.datetime.strptime(k, '%Y-%m-%d')
                data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                            float(v['4. close']),float(v['1. open'])]
                df.loc[-1,:] = data_row
                df.index = df.index + 1
            print('Data saved to : %s'%file_to_save)        
            df.to_csv(file_to_save)

        

get_data_from_av(True)