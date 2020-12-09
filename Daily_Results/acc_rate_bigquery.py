# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 21:50:59 2020

@author: Yuke
"""

import pandas as pd
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
from datetime import timezone
from itertools import islice
from dateutil.relativedelta import relativedelta

all_token = pd.read_csv('all-time-price_27_tokens.csv')
coin = all_token[all_token['Token']=='CS']
coin['Time'] = pd.to_datetime(coin['Time'])
#lend = lend.set_index('Unnamed: 0')
#del lend.index.name #if this line reports error, use the next line
# lend.columns.name = None
df = pd.read_csv('CS.csv')  #39945 Wallets
#df = df.T
#df = df.set_index('Unnamed: 0')
#del df.index.name #if this line reports error, use the next line
# df.columns.name = None
date = df['entry_time'].tolist()
entry = []
for item in date:
    #for unixtime in item:
    entry.append(item.split(' ')[0])
df['Date'] = entry
df['Date'] = pd.to_datetime(df['Date'])
keys, counts = np.unique(entry, return_counts=True)
date_wallet = pd.DataFrame()
date_wallet['Date'] = keys
date_wallet['Date'] = pd.to_datetime(date_wallet['Date'])
date_wallet['Count'] = counts
date_wallet = date_wallet.sort_values('Date')
print(date_wallet)

daily = pd.merge(date_wallet, coin, how='inner', left_on='Date', right_on='Time')
daily = daily.drop('Time',axis=1)
daily.set_index(pd.DatetimeIndex(daily['Date']), inplace=True)
daily = daily.set_index('Date')
daily['7days_cum_sum'] = daily['Count'].cumsum()
idx =pd.date_range(min(entry), max(entry))
daily = daily.reindex(idx, fill_value=0)
#pd.options.display.float_format = '{:,.2f}'.format
daily['7days_acc_rate'] = daily['7days_cum_sum'].pct_change(periods=7)
daily['price_change'] = daily['Price'].pct_change(periods=7)
daily = daily.sort_values('7days_acc_rate')
daily['7days_acc_rate']= daily['7days_acc_rate'].fillna(0)
daily['7days_acc_rate'].replace(np.inf, 0, inplace=True)
#daily['7days_cum_perc'] = 
daily = daily.sort_values('7days_acc_rate', ascending=False)
daily = daily[daily['7days_cum_sum']!=0]
daily['7days_acc_rate'] = (100. * daily['7days_acc_rate']).round(1).astype(str) + '%'
daily['price_change'] = (100. * daily['price_change']).round(1).astype(str) + '%'
print(daily)
daily.to_csv('CS_top_daily.csv')

# Now get 10 days with the highest acc_rate and find the dates of 7 days advanced
timess = []
for index, date in islice(daily.iterrows(),0,10):
    timess.append(index.strftime('%Y-%m-%d'))
days7_before = []
for item in timess:
    days7_before.append(datetime.strptime(item, '%Y-%m-%d').date() + relativedelta(days=-8))


potential_leaders = pd.DataFrame()
for item in days7_before:
    potential_leaders = potential_leaders.append(df[df['Date']==datetime.strftime(item,'%Y-%m-%d')])
print(potential_leaders)
potential_leaders['Wallet_id'].to_csv('CS_leaders.csv',index=False)

'''
#plt.figure(figsize=(12,6))
#date_wallet.plot(x='Date', y='Count',figsize=(14,6))
#plt.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#plt.figure(figsize=(12,6))
#plt.bar(keys, counts)
#plt.setp(keys.get_xticklabels(), rotation=30, horizontalalignment='right')
#plt.xticks(rotation=60)
#plt.show()

#fig, ax1 = plt.subplots(figsize=(12,6))
#ax1.bar(date_wallet['Date'], date_wallet['Count'])
#fig.autofmt_xdate()
'''