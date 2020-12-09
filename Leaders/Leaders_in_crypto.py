# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:45:40 2020

@author: Yuke
"""
import pandas as pd
import glob

# glob.glob('data*.csv') - returns List[str]
# pd.read_csv(f) - returns pd.DataFrame()
# for f in glob.glob() - returns a List[DataFrames]
# pd.concat() - returns one pd.DataFrame()
df = pd.concat([pd.read_csv(f,header=None) for f in glob.glob('*leaders.csv')], ignore_index = True)
leaders = pd.value_counts(df[0])
leaders.to_csv('Leaders.csv',columns=['Wallet_id','number_of_leading_markets'])