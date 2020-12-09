# Crypto-Laggard-and-Leader-Project
- The team is focusing on crypto-impact sustainability, in other words, cryptocurrency market analysis. 
- Our objective is to utilize the leaders and laggards’ analysis to help potential investors make decisions by minimizing the risk of investment. Leaders are the first investors who buy the currency and laggards are the ones who follow the leaders. 

- To achieve this objective, we had to finish two tasks, first, data collection; and second, calculation of accelerating rate and the price change. 

- For the first step, I applied API and JSON web-scraping in Python (See file "transaction") to gather data from different sources, including Etherscan, Coingecko, and BigQuery. The transaction data I retrieved from Google cloud platform with BigQuery contain 87 Gigabytes for all crypto currency markets. In folder "Wallet_entrydate_in_each_market", there are files for the entry date of all wallets in 19 different markets.

- Then, I cleaned and merged the datasets to get the dates, the daily price of a token, daily number of new investors, and cumulative new investors. In the next step, I used the table to calculate the accelerating rate, which is the percentage change in new investors between two different dates. The dates with higher accelerating rate were supposed to be the days that most followers entered the markets. Then we were able to find investors as potential leaders among the investors who entered the markets 7 days before these top accelerated dates. (See file "acc_rate_bigquery")

- From the combination of all potential leaders' files created by the previous step, we can find wallets that lead in mulpitle token markets. These wallets can be confirmed as leaders in crypto markets. (See file "Leaders_in_crypto")
