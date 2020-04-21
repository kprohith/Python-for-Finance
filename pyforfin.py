import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
style.use('ggplot')

start = dt.datetime(2019, 1 ,1)
end = dt.datetime.now()

df = web.DataReader("AAPL", 'av-daily', start, end, access_key='xxxx')

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
df['100ma'] = df['close'].rolling(window=10, min_periods=0).mean()
print(df.head())
"""ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.plot(df.index, df['close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['volume'])
"""
df_ohlc = df['close'].resample('10D').ohlc()
df_volume = df['volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)

df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)


ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)
plt.show()





