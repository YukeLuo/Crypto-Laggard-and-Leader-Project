import etherscan
from etherscan.accounts import Account
import json
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import urllib.request
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
import statistics
import time
from pycoingecko import CoinGeckoAPI
from itertools import islice
import csv

start_time = datetime.now()
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    #Call in a loop to create terminal progress bar
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

     
        
token_file = pd.read_csv('available_tokens.csv', header=None)
token_id = token_file[0].to_list()
token_index = token_file.index.to_list()
token_name = token_file[1].to_list()
coin_first_date = pd.read_csv('coin_first_date.csv',header=None)
first_date = coin_first_date[0].to_list()
holders = pd.read_csv('ethlend_holders.csv')
wallets = []
i = 0
for index, row in islice(holders.iterrows(),0,70000):
    if row['HolderAddress'] not in wallets:
        wallets.append(row['HolderAddress'])
#print("Number of wallets to process: " + str(len(wallets)))

# some wallets entered the market less than 8 weeks, fill in 0s for mean calculation.
def extend(some_list, target_len):
    return some_list[:target_len] + [[0,float('inf')]]*(target_len - len(some_list))

with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']
wallet_data = {} # maps wallet address to dictionary mapping every token that wallet holds to the timestamp of when the wallet first received that token
progress = 0
printProgressBar(0, len(wallets), prefix = 'Progress:', suffix = 'Complete', length = 50)
for address in wallets:
    #time.sleep(0.1)
    printProgressBar(progress + 1, len(wallets), prefix = 'Progress:', suffix = 'Complete', length = 50)
    progress += 1
    api = Account(address=address, api_key=key)
    transactions = api.get_transaction_page(page=1, offset=10000, sort='des', erc20=True)
    tokens_owned = {}
  # print(transactions)
    for tran in reversed(transactions):
        if tran['to'] == address:
            if tran['tokenSymbol'] not in tokens_owned.keys():
                #print(tran['tokenSymbol'])
                if tran['tokenSymbol'] == 'LEND':
    # tokens_owned[tran['tokenName']] = datetime.utcfromtimestamp(int(tran['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
                #print(tran['tokenSymbol'])
                
                    tokens_owned[tran['tokenSymbol']] = tran['timeStamp']
    if len(tokens_owned) >= 1:
        wallet_data[address] = tokens_owned

df = pd.DataFrame(wallet_data)
df = df.T
df.to_csv('LEND4wto5w.csv')