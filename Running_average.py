import etherscan
from etherscan.accounts import Account
import json
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import urllib.request
import json
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from datetime import datetime
import statistics

from pycoingecko import CoinGeckoAPI


token_file = pd.read_csv('available_tokens.csv', header=None)
token_id = token_file[0].to_list()
token_index = token_file.index.to_list()
token_name = token_file[1].to_list()
holders = pd.read_csv('ethlend_holders.csv')
wallets = []
i = 0
for index, row in holders.iterrows():
    if row['HolderAddress'] not in wallets:
        wallets.append(row['HolderAddress'])
#        i += 1
#        if i == 10: 
#            break

print("Number of wallets to process: " + str(len(wallets)))

# some wallets entered the market less than 8 weeks, fill in 0s for mean calculation.
def extend(some_list, target_len):
    return some_list[:target_len] + [[0,float('inf')]]*(target_len - len(some_list))

with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']
wallet_data = {} # maps wallet address to dictionary mapping every token that wallet holds to the timestamp of when the wallet first received that token

for address in wallets:
    api = Account(address=address, api_key=key)
    transactions = api.get_transaction_page(page=1, offset=10000, sort='des', erc20=True)
    tokens_owned = {}
  # print(transactions)
    for tran in reversed(transactions):
        if tran['to'] == address:
            if tran['tokenSymbol'] not in tokens_owned.keys():
    # tokens_owned[tran['tokenName']] = datetime.utcfromtimestamp(int(tran['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
                tokens_owned[tran['tokenSymbol']] = tran['timeStamp']
  
    #print("tokens_owned",tokens_owned)
    if len(tokens_owned) >= 5:
        wallet_data[address] = tokens_owned
#print("wallet_data:",wallet_data)

wallet_id = []
market_count = []
token_names = []
trend_8wk_b = []
trend_7wk_b = []
trend_6wk_b = []
trend_5wk_b = []
trend_4wk_b = []
trend_3wk_b = []
trend_2wk_b = []
trend_1wk_b = []

trend_1wk_a = []
trend_2wk_a = []
trend_3wk_a = []
trend_4wk_a = []
trend_5wk_a = []
trend_6wk_a = []
trend_7wk_a = []
trend_8wk_a = []

trends = [trend_8wk_b, trend_7wk_b, trend_6wk_b, trend_5wk_b, trend_4wk_b, trend_3wk_b, trend_2wk_b, trend_1wk_b,
          trend_1wk_a, trend_2wk_a, trend_3wk_a, trend_4wk_a, trend_5wk_a, trend_6wk_a, trend_7wk_a, trend_8wk_a]

# wallet_data = {'0x1da1473a63da444546ab8a6584cbe8ba7667f065': {'bitcoin': '1582156800', 'aidcoin': '1582156800'},
#                '0x1da1473a63da444546ab8a6584cbe8ba7667f064': {'bitcoin': '1582326800', 'aidcoin': '1582187800'}}
df = pd.DataFrame()
token_price_data = {} # Maps token name to json containing all-time price data

for wallet, data in wallet_data.items():
    #print(data)
    print(wallet)
    
    #wallet_id.append(wallet)

    run_8wk_b = []
    run_7wk_b = []
    run_6wk_b = []
    run_5wk_b = []
    run_4wk_b = []
    run_3wk_b = []
    run_2wk_b = []
    run_1wk_b = []

    run_1wk_a = []
    run_2wk_a = []
    run_3wk_a = []
    run_4wk_a = []
    run_5wk_a = []
    run_6wk_a = []
    run_7wk_a = []
    run_8wk_a = []

    runs = [run_8wk_b, run_7wk_b, run_6wk_b, run_5wk_b, run_4wk_b, run_3wk_b, run_2wk_b, run_1wk_b,
            run_1wk_a, run_2wk_a, run_3wk_a, run_4wk_a, run_5wk_a, run_6wk_a, run_7wk_a, run_8wk_a]
    token_count = 0
    for token, entry_date in data.items():
        #token = token.lower()
        #print(token)
        if token in token_name:
            wallet_id.append(wallet)
            ids = token_id[token_name.index(token)]
            token_names.append(ids)
            #ids = token_file.loc[token_file[1]==token,0].item()
            #ids = token_file[token_file[1]==token][0].apply(lambda x: "'" + str(x) + "'")
            #ids = "'",ids, "'"
            print(ids)
            cg = CoinGeckoAPI()
            days_50 = 4881600 #56.5 days, just over 8 weeks
            entry = datetime.utcfromtimestamp(int(entry_date)).strftime('%d-%m-%Y')
            price_request = cg.get_coin_history_by_id(ids, str(entry))
            entry_price = float(price_request.get('market_data')['current_price']['usd'])

            request = cg.get_coin_market_chart_range_by_id(ids,'usd', int(entry_date) - days_50, int(entry_date) + days_50)
            content = request.get('prices')
            token_price_data[ids] = content

            wk8b = content[0:7]
            wk7b = content[7:14]
            wk6b = content[14:21]
            wk5b = content[21:28]
            wk4b = content[28:35]
            wk3b = content[35:42]
            wk2b = content[42:49]
            wk1b = content[49:56]

            wk1a = content[56:63]
            wk2a = content[63:70]
            wk3a = content[70:77]
            wk4a = content[77:84]
            wk5a = content[84:91]
            wk6a = content[91:98]
            wk7a = content[98:105]
            wk8a = content[105:112]

            trend_data = [wk8b, wk7b, wk6b, wk5b, wk4b, wk3b, wk2b, wk1b, wk1a, wk2a, wk3a, wk4a, wk5a, wk6a, wk7a, wk8a]
            
            for index, segment in enumerate(trend_data):
                prices = []
                #if len(segment) < 7:
                #    print("those < 7:", segment)
                segment = extend(segment,7)
                for day in segment:
                    prices.append(day[1])

    # Find running weekly averages
                    run_avg = statistics.mean(prices)
    # Find percent change from entry price
                    if index < 8:
                        runs[index].append((entry_price - run_avg)/run_avg)
                    else:
                        runs[index].append((entry_price - run_avg)/run_avg)
                        token_count += 1
            
            for index, segment in enumerate(runs):
                trends[index].append(statistics.mean(segment))
        else:
            print('Token not found, skipping')
        market_count.append(token_count)
        #print('FINISH HERE')


df['Wallet'] = wallet_id
df['Token'] = token_names
#df['Market Count'] = market_count
df['Avg. Price 8 Wks Prior'] = trend_8wk_b
df['Avg. Price 7 Wks Prior'] = trend_7wk_b
df['Avg. Price 6 Wks Prior'] = trend_6wk_b
df['Avg. Price 5 Wks Prior'] = trend_5wk_b
df['Avg. Price 4 Wks Prior'] = trend_4wk_b
df['Avg. Price 3 Wks Prior'] = trend_3wk_b
df['Avg. Price 2 Wks Prior'] = trend_2wk_b
df['Avg. Price 1 Wk Prior'] = trend_1wk_b

df['Avg. Price 1 Wk After'] = trend_1wk_a
df['Avg. Price 2 Wks After'] = trend_2wk_a
df['Avg. Price 3 Wks After'] = trend_3wk_a
df['Avg. Price 4 Wks After'] = trend_4wk_a
df['Avg. Price 5 Wks After'] = trend_5wk_a
df['Avg. Price 6 Wks After'] = trend_6wk_a
df['Avg. Price 7 Wks After'] = trend_7wk_a
df['Avg. Price 8 Wks After'] = trend_8wk_a

print(df)
df.to_csv('Running_Average_16weeks_Results.csv',index=0)