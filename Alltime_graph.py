# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:46:45 2020

@author: Yuke_Luo
"""

import pandas as pd

alltime = pd.read_csv('all-time-price_27_tokens.csv')
print(alltime)
for title, group in alltime.groupby('Token'):
    group.plot(x='Time', y='Price', title=title)