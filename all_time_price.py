# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:46:45 2020

@author: Yuke_Luo
"""

from pycoingecko import CoinGeckoAPI
import datetime
import pandas as pd 

def get_token(token_name):
    req = CoinGeckoAPI()
    request = req.get_coin_market_chart_by_id(id=token_name,vs_currency='usd',days='max') #Data up to number of days ago (eg. 1,14,30,max)
    #Minutely data will be used for duration within 1 day, Hourly data will be used for duration between 1 day and 90 days, Daily data will be used for duration above 90 days.
    content = request.get('prices')
    
    
    unixtime = []
    price = []
    for u, p in content:
        unixtime.append(str(u))
        price.append(p)
    
    actual_time = []
    for item in unixtime:
        date = datetime.datetime.utcfromtimestamp(int(item[:-3]))
        actual_time.append(date.strftime('%Y-%m-%d'))
    
    
    df = pd.DataFrame()
    df['Time'] = actual_time
    df['Price'] = price
    df['Token'] = token_name
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    
    return df

token_names = pd.read_csv('available_tokens.csv', header=None)
tokens = token_names[0].to_list()
#coin = ['aidcoin']
df = pd.DataFrame()

for item in tokens: # Try [0:10] if don't want to go thru too many tokens (also for time saving):
    print(item)
    a = get_token(item)
    #print(a.head())
    df = df.append(a)
print(df)

"""
### Minimum Price ###
df[df['Price'] == df['Price'].min()]
### Maximum Price ###
df[df['Price'] == df['Price'].max()]
"""

""" Plot coins prices """
"""
df['Time'] = pd.to_datetime(df['Time'],format='%Y-%m-%d')
df = df.pivot(index='Time', columns='Token', values='Price')
df.set_index('Time', inplace=True)
print(df.plot(figsize=(10,5)))
"""