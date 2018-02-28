#!/usr/bin/env python
# Author: Emiliano Sauvisky <esauvisky@gmail.com>.
# Description: Verifica oportunidades de arbitragem em bolsas BTC brasileiras

## Imports
import os
import sys
import time
import requests
import credentials
from pprint import pprint
import mbapi.tapi as mbt
import foxapi.foxbit as fox
# Things to make libnotify work
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
Notify.init('Arbit')

## Global Constants
# TODO: get fees data from bitvalor
feesData = {'MBT': {'name': 'Mercado Bitcoin', 'color': 'e6194b', 'url': 'https://www.mercadobitcoin.com.br', 'url_book': 'https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/', 'fees': {'in_BRL': [0.0199, 2.9], 'in_BTC': [0, 0], 'out_BRL': [0.0199, 2.9], 'out_BTC': [0, 0], 'trade_book': [0.003, 0], 'trade_market': [0.007, 0]}}, 'B2U': {'name': 'BitcoinToYou', 'color': '0082c8', 'url': 'https://www.bitcointoyou.com', 'url_book': 'https://broker.bitcointoyou.com/Negociacoes/externo', 'fees': {'in_BRL': [0.0189, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0189, 0], 'out_BTC': [0, 0], 'trade_book': [0.0025, 0], 'trade_market': [0.006, 0]}}, 'BAS': {'name': 'Basebit', 'color': 'aaffc3', 'url': 'https://www.basebit.com.br', 'url_book': 'https://www.basebit.com.br', 'fees': {'in_BRL': [0.0149, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0149, 0], 'out_BTC': [0, 0], 'trade_book': [0.0025, 0], 'trade_market': [0.006, 0]}}, 'FOX': {'name': 'FoxBit', 'color': 'f58231', 'url': 'http://foxbit.com.br/', 'url_book': 'https://foxbit.exchange/#market', 'fees': {'in_BRL': [0.0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0139, 0], 'out_BTC': [0, 0.0002], 'trade_book': [0.0025, 0], 'trade_market': [0.005, 0]}}, 'BIV': {'name': 'Bitinvest', 'color': 'e6beff', 'url': 'https://www.bitinvest.com.br', 'url_book': 'https://www.bitinvest.com.br/exchange/orders/negotiations', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0099, 0], 'out_BTC': [0, 0], 'trade_book': [0.003, 0], 'trade_market': [0.003, 0]}}, 'FLW': {'name': 'flowBTC', 'color': '808080', 'url': 'https://trader.flowbtc.com', 'url_book': 'https://trader.flowbtc.com', 'fees': {'in_BRL': [0.005, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0119, 8], 'out_BTC': [0, 0.0015], 'trade_book': [0.0035, 0], 'trade_market': [0.0035, 0]}}, 'NEG': {'name': 'Negocie Coins', 'color': 'd2f53c', 'url': 'https://www.negociecoins.com.br', 'url_book': 'http://www.negociecoins.com.br/negociacoes', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.009, 8.9], 'out_BTC': [0, 0.001], 'trade_book': [0.003, 0], 'trade_market': [0.004, 0]}}, 'LOC': {'name': 'LocalBitcoins', 'color': '911eb4', 'url': 'https://localbitcoins.com/', 'url_book': 'https://localbitcoins.com/', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0.01, 0], 'trade_market': [0, 0]}}, 'ARN': {'name': 'Arena Bitcoin', 'color': 'ffd8b1', 'url': 'http://www.arenabitcoin.com.br/', 'url_book': 'https://www.arenabitcoin.com/markets/btccny', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.001, 0], 'out_BTC': [0, 0.0005], 'trade_book': [0.0015, 0], 'trade_market': [0.0015, 0]}}, 'PAX': {'name': 'Paxful', 'color': 'ffe119', 'url': 'https://paxful.com/', 'url_book': 'https://paxful.com/buy-bitcoin', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0.01, 0], 'trade_market': [0, 0]}}, 'BSQ': {'name': 'Bitsquare', 'color': '800000', 'url': 'https://bitsquare.io/', 'url_book': 'https://market.bitsquare.io/?market=btc_brl', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0, 0.0005], 'trade_market': [0, 0.001]}}, 'BTD': {'name': 'BitcoinTrade', 'color': '000000', 'url': 'https://bitcointrade.com.br/', 'url_book': 'https://bitcointrade.com.br/marketplace', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0099, 4.9], 'out_BTC': [0, 0], 'trade_book': [0.005, 0], 'trade_market': [0.005, 0]}}, 'BZX': {'name': 'Braziliex', 'color': '3cb44b', 'url': 'https://braziliex.com/', 'url_book': 'https://braziliex.com', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0025, 9], 'out_BTC': [0, 0.001], 'trade_book': [0.005, 0], 'trade_market': [0.005, 0]}}}
orderBookStatsURL = 'https://api.bitvalor.com/v1/order_book_stats.json'
allowedExchanges = ['FOX', 'MBT']
sellingBTCQuantity = 0.001
mbtAuth = mbt.Auth(id=credentials.MercadoBitcoin['id'],
                   pin=credentials.MercadoBitcoin['pin'],
                   secret=credentials.MercadoBitcoin['secret'])
foxAuth = fox.Auth(id=credentials.FoxBit['key'],
                   secret=credentials.FoxBit['secret'])
mbtTrade = mbt.Trade(mbtAuth)


def fetch_balances():
    '''
    Updates BTC and BRL balance for each exchange in allowedExchanges
    '''
    # Prefills the dict
    returnValue = {e: {'BRL': 0, 'BTC': 0} for e in allowedExchanges}

    # Loops through exchanges and grabs each respective balance
    for exchange in allowedExchanges:
        if exchange == 'MBT':
            mbtInfo = mbtTrade.get_account_info()
            returnValue['MBT']['BRL'] = float(mbtInfo.data['balance']['brl']['available'])
            returnValue['MBT']['BTC'] = float(mbtInfo.data['balance']['btc']['available'])
        elif exchange == 'FOX':
            foxInfo = fox.get_account_info(foxAuth)
            returnValue['FOX']['BRL'] = foxInfo['Responses'][0]['4']['BRL']
            returnValue['FOX']['BTC'] = foxInfo['Responses'][0]['4']['BTC']
        else:
            print('[ERROR] This exchange is not implemented yet.')
            sys.exit()

    return returnValue


def fetch_orderbooks():
    '''
    Fetches order book data from BitValor
    '''
    successful = False
    attempt = 1
    while not successful:
        try:
            #orderBookStatsJSON = {'FOX': {'ask': 33900, 'bid': 33800}, 'MBT': {'ask': 34900, 'bid': 34800}}
            response = requests.get(orderBookStatsURL)
            if response.status_code == requests.codes.ok:
                successful = True
                break
            else:
                print('[ERROR] Got bad request status code: ' + response.status_code)
        except Exception as e:
            print('[ERROR] Something bad happened while fetching the order book... Maybe connection error?')

        print('Trying again in ' + str(2 ** attempt) + ' seconds...')
        time.sleep(2 ** attempt)
        attempt += 1

    if attempt > 1:
        print('Successfully connected now!')
    orderBookStatsJSON = response.json()
    # Filters orderBookStatsJSON to contain only selected exchanges with bid and ask prices
    return {exchange: {'bid': orderBookStatsJSON[exchange]['bid'], 'ask': orderBookStatsJSON[exchange]['ask']} for exchange in allowedExchanges}


## Main Code
def main():
    global balances
    exchanges = fetch_orderbooks()
    #exchanges = {'FOX': {'bid': 33100, 'ask': 33200}, 'MBT': {'bid': 34100, 'ask': 34200}}

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

            if (totalSPrice > totalBPrice) and profit > 0.1:
                print('Arbitrage opportunity (' + str(profit) + '%) | ' + time.ctime())
                print('Sell in ' + sExchange + ' at ' + str(sPrice['bid']) + '\t (you will receive ' + str(round(totalSPrice)) + ')')
                print('Buy  in ' + bExchange + ' at ' + str(bPrice['ask']) + '\t (you will pay     ' + str(round(totalBPrice)) + ')')

                notification = Notify.Notification.new('Arbitrage Opportunity (' + str(profit) + '%)',
                                                       'SELL in\t' + sExchange + '\tat\t' + str(format(sPrice['bid'], '.2f')) + '\t(you will receive \t' + str(round(totalSPrice)) + ')\n' +
                                                       'BUY  in\t' + bExchange + '\tat\t' + str(format(bPrice['ask'], '.2f')) + '\t(you will pay     \t' + str(round(totalBPrice)) + ')',
                                                       current_dir + '/profit.png')
                notification.set_urgency(2)
                notification.show()
                os.system('paplay beep.wav')

                sellingTotalBRL = sellingBTCQuantity * totalSPrice
                print('Placing ' + sellingBTCQuantity + ' BTC sell order in ' + sExchange + '... (' + sellingTotalBRL + ' BRL)')
                if sExchange == 'MBT':
                    mbtOrder = mbtTrade.place_sell_order(quantity=sellingBTCQuantity, limit=sPrice['bid'])
                    print(mbtOrder.data)
                elif sExchange == 'FOX':
                    fox.place_sell_order(quantity=sellingBTCQuantity, limit=sPrice['bid'], auth=foxAuth)

                buyingBTCQuantity = sellingTotalBRL / totalBPrice
                buyingTotalBRL = buyingBTCQuantity * totalBPrice
                print('Placing ' + buyingBTCQuantity + ' BTC buy order in ' + bExchange + '... (' + buyingTotalBRL + ' BRL)')
                if bExchange == 'MBT':
                    mbtOrder = mbtTrade.place_buy_order(quantity=buyingBTCQuantity, limit=bPrice['ask'])
                    print(mbtOrder.data)
                elif bExchange == 'FOX':
                    fox.place_buy_order(quantity=buyingBTCQuantity, limit=bPrice['ask'], auth=foxAuth)

                # TODO: Wait for orders to be executed before going on
                print("We're done for now, take a look to see if it worked! Balances below: \n")
                # Refresh balances:
                balances = fetch_balances()
                pprint(balances)
                sys.exit()


## The Loop
try:
    # Changes PWD to Arbit dir
    current_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    os.chdir(current_dir)

    # Fetches balances only once at start
    balances = fetch_balances()
    pprint(balances)

    while True:
        main()
        time.sleep(60)
except KeyboardInterrupt:
    print('\rExiting...')

