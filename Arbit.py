#!/usr/bin/env python
# Author: Emiliano Sauvisky <esauvisky@gmail.com>.
# Description: Verifica oportunidades de arbitragem em bolsas BTC brasileiras

## Imports
#import json
#from pprint import pprint
import os
import requests

# Things to make libnotify work
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
Notify.init('Arbit')

# Changes PWD to Arbit dir
current_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
os.chdir(current_dir)


## Global Constants
feesData = {'MBT': {'name': 'Mercado Bitcoin', 'color': 'e6194b', 'url': 'https://www.mercadobitcoin.com.br', 'url_book': 'https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/', 'fees': {'in_BRL': [0.0199, 2.9], 'in_BTC': [0, 0], 'out_BRL': [0.0199, 2.9], 'out_BTC': [0, 0], 'trade_book': [0.003, 0], 'trade_market': [0.007, 0]}}, 'B2U': {'name': 'BitcoinToYou', 'color': '0082c8', 'url': 'https://www.bitcointoyou.com', 'url_book': 'https://broker.bitcointoyou.com/Negociacoes/externo', 'fees': {'in_BRL': [0.0189, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0189, 0], 'out_BTC': [0, 0], 'trade_book': [0.0025, 0], 'trade_market': [0.006, 0]}}, 'BAS': {'name': 'Basebit', 'color': 'aaffc3', 'url': 'https://www.basebit.com.br', 'url_book': 'https://www.basebit.com.br', 'fees': {'in_BRL': [0.0149, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0149, 0], 'out_BTC': [0, 0], 'trade_book': [0.0025, 0], 'trade_market': [0.006, 0]}}, 'FOX': {'name': 'FoxBit', 'color': 'f58231', 'url': 'http://foxbit.com.br/', 'url_book': 'https://foxbit.exchange/#market', 'fees': {'in_BRL': [0.0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0139, 0], 'out_BTC': [0, 0.0002], 'trade_book': [0.0025, 0], 'trade_market': [0.005, 0]}}, 'BIV': {'name': 'Bitinvest', 'color': 'e6beff', 'url': 'https://www.bitinvest.com.br', 'url_book': 'https://www.bitinvest.com.br/exchange/orders/negotiations', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0099, 0], 'out_BTC': [0, 0], 'trade_book': [0.003, 0], 'trade_market': [0.003, 0]}}, 'FLW': {'name': 'flowBTC', 'color': '808080', 'url': 'https://trader.flowbtc.com', 'url_book': 'https://trader.flowbtc.com', 'fees': {'in_BRL': [0.005, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0119, 8], 'out_BTC': [0, 0.0015], 'trade_book': [0.0035, 0], 'trade_market': [0.0035, 0]}}, 'NEG': {'name': 'Negocie Coins', 'color': 'd2f53c', 'url': 'https://www.negociecoins.com.br', 'url_book': 'http://www.negociecoins.com.br/negociacoes', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.009, 8.9], 'out_BTC': [0, 0.001], 'trade_book': [0.003, 0], 'trade_market': [0.004, 0]}}, 'LOC': {'name': 'LocalBitcoins', 'color': '911eb4', 'url': 'https://localbitcoins.com/', 'url_book': 'https://localbitcoins.com/', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0.01, 0], 'trade_market': [0, 0]}}, 'ARN': {'name': 'Arena Bitcoin', 'color': 'ffd8b1', 'url': 'http://www.arenabitcoin.com.br/', 'url_book': 'https://www.arenabitcoin.com/markets/btccny', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.001, 0], 'out_BTC': [0, 0.0005], 'trade_book': [0.0015, 0], 'trade_market': [0.0015, 0]}}, 'PAX': {'name': 'Paxful', 'color': 'ffe119', 'url': 'https://paxful.com/', 'url_book': 'https://paxful.com/buy-bitcoin', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0.01, 0], 'trade_market': [0, 0]}}, 'BSQ': {'name': 'Bitsquare', 'color': '800000', 'url': 'https://bitsquare.io/', 'url_book': 'https://market.bitsquare.io/?market=btc_brl', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0, 0.0005], 'trade_market': [0, 0.001]}}, 'BTD': {'name': 'BitcoinTrade', 'color': '000000', 'url': 'https://bitcointrade.com.br/', 'url_book': 'https://bitcointrade.com.br/marketplace', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0099, 4.9], 'out_BTC': [0, 0], 'trade_book': [0.005, 0], 'trade_market': [0.005, 0]}}, 'BZX': {'name': 'Braziliex', 'color': '3cb44b', 'url': 'https://braziliex.com/', 'url_book': 'https://braziliex.com', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0025, 9], 'out_BTC': [0, 0.001], 'trade_book': [0.005, 0], 'trade_market': [0.005, 0]}}}
orderBookStatsURL = 'https://api.bitvalor.com/v1/order_book_stats.json'
allowedExchanges = ['FOX', 'MBT']


## Fetch Data from BitValor
def fetch_data():
    response = requests.get(orderBookStatsURL)
    orderBookStatsJSON = response.json()
    #orderBookStatsJSON = {'FOX': {'ask': 33900, 'bid': 33800}, 'MBT': {'ask': 34900, 'bid': 34800}}

    # Filters orderBookStatsJSON to contain only selected exchanges with bid and ask prices
    return {exchange: {'bid': orderBookStatsJSON[exchange]['bid'], 'ask': orderBookStatsJSON[exchange]['ask']} for exchange in allowedExchanges}


##### MAIN LOOP #####
while True:
    exchanges = fetch_data()

    # Loops through the exchange where you'll buy
    for bExchange, bPrice in exchanges.items():
        for sExchange, sPrice in exchanges.items():
            # Don't compare the exchange against itself
            if bExchange == sExchange:
                continue

            # The fee percentage for buying
            bFee = feesData[bExchange]['fees']['trade_market'][0]
            # The fee percentage for selling
            sFee = feesData[sExchange]['fees']['trade_market'][0]

            # The price people are asking for 1 btc at market (plus the fees):
            totalBPrice = bPrice['ask'] + (bFee * bPrice['ask'])
            # The price people are willing to pay for 1 btc at the market (less the fees):
            totalSPrice = sPrice['bid'] - (sFee * sPrice['bid'])

            # Calculates the profit, if any (including fees)
            profit = round((((totalSPrice / totalBPrice) - 1) * 100), 2)

            if (totalSPrice > totalBPrice):  # and (profit > 0.9):
                print('Arbitrage opportunity (' + str(profit) + '%)')
                print('Buy  in ' + bExchange + ' at ' + str(bPrice['ask']) + '\t (you will pay     ' + str(round(totalBPrice)) + ')')
                print('Sell in ' + sExchange + ' at ' + str(sPrice['bid']) + '\t (you will receive ' + str(round(totalSPrice)) + ')')
                notification = Notify.Notification.new('Arbitrage Opportunity (' + str(profit) + '%)',
                                                       'BUY  in\t' + bExchange + '\tat\t' + str(bPrice['ask']) + '\t(you will pay \t\t' + str(round(totalBPrice)) + ')\n' +
                                                       'SELL in\t' + sExchange + '\tat\t' + str(sPrice['bid']) + '\t(you will receive \t' + str(round(totalSPrice)) + ')',
                                                       current_dir + '/profit.png')
                notification.set_urgency(2)
                notification.show()

