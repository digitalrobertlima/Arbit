#!/usr/bin/env python
# Author: Emiliano Sauvisky <esauvisky@gmail.com>.
# Description: Does arbitrage between brazilian BTC exchanges


# TODO-1: Fetch prices from each's exchange API instead of using BitValor
#         Fetch fees data from each's exchanges API as well

# TODO-2: use the balance for calculating the optimum quantity to trade:
# if the profit is low, use a lower ammount
# if the profit is huge, go all-in and use all the funds available.
# Something like:
# 0.5% -> 0.001 BTC
# 3%+  -> Half
# 5%+  -> All-in

# TODO-3: make 2 custom functions for setting up the orders:
# 1 for taker orders (market buy/sell, just like below)
# 2 for maker orders (limit buy/sell, a bit riskier but more profit)
# So, if the profit is low (<1%), try #2, to maximize the profit
# if it's high, go straight for market orders, because we want speed.
# If using #2, we need to wait until the orders are executed, before going on.

## Imports
import os
import sys
import time
import requests
import credentials
from pprint import pprint
import mbapi.tapi as mbt
import foxapi.tapi as fox

## Global Constants
feesData = {'MBT': {'name': 'Mercado Bitcoin', 'color': 'e6194b', 'url': 'https://www.mercadobitcoin.com.br', 'url_book': 'https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/', 'fees': {'in_BRL': [0.0199, 2.9], 'in_BTC': [0, 0], 'out_BRL': [0.0199, 2.9], 'out_BTC': [0, 0], 'trade_book': [0.003, 0], 'trade_market': [0.007, 0]}}, 'B2U': {'name': 'BitcoinToYou', 'color': '0082c8', 'url': 'https://www.bitcointoyou.com', 'url_book': 'https://broker.bitcointoyou.com/Negociacoes/externo', 'fees': {'in_BRL': [0.0189, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0189, 0], 'out_BTC': [0, 0], 'trade_book': [0.0025, 0], 'trade_market': [0.006, 0]}}, 'BAS': {'name': 'Basebit', 'color': 'aaffc3', 'url': 'https://www.basebit.com.br', 'url_book': 'https://www.basebit.com.br', 'fees': {'in_BRL': [0.0149, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0149, 0], 'out_BTC': [0, 0], 'trade_book': [0.0025, 0], 'trade_market': [0.006, 0]}}, 'FOX': {'name': 'FoxBit', 'color': 'f58231', 'url': 'http://foxbit.com.br/', 'url_book': 'https://foxbit.exchange/#market', 'fees': {'in_BRL': [0.0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0139, 0], 'out_BTC': [0, 0.0002], 'trade_book': [0.0025, 0], 'trade_market': [0.005, 0]}}, 'BIV': {'name': 'Bitinvest', 'color': 'e6beff', 'url': 'https://www.bitinvest.com.br', 'url_book': 'https://www.bitinvest.com.br/exchange/orders/negotiations', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0099, 0], 'out_BTC': [0, 0], 'trade_book': [0.003, 0], 'trade_market': [0.003, 0]}}, 'FLW': {'name': 'flowBTC', 'color': '808080', 'url': 'https://trader.flowbtc.com', 'url_book': 'https://trader.flowbtc.com', 'fees': {'in_BRL': [0.005, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0119, 8], 'out_BTC': [0, 0.0015], 'trade_book': [0.0035, 0], 'trade_market': [0.0035, 0]}}, 'NEG': {'name': 'Negocie Coins', 'color': 'd2f53c', 'url': 'https://www.negociecoins.com.br', 'url_book': 'http://www.negociecoins.com.br/negociacoes', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.009, 8.9], 'out_BTC': [0, 0.001], 'trade_book': [0.003, 0], 'trade_market': [0.004, 0]}}, 'LOC': {'name': 'LocalBitcoins', 'color': '911eb4', 'url': 'https://localbitcoins.com/', 'url_book': 'https://localbitcoins.com/', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0.01, 0], 'trade_market': [0, 0]}}, 'ARN': {'name': 'Arena Bitcoin', 'color': 'ffd8b1', 'url': 'http://www.arenabitcoin.com.br/', 'url_book': 'https://www.arenabitcoin.com/markets/btccny', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.001, 0], 'out_BTC': [0, 0.0005], 'trade_book': [0.0015, 0], 'trade_market': [0.0015, 0]}}, 'PAX': {'name': 'Paxful', 'color': 'ffe119', 'url': 'https://paxful.com/', 'url_book': 'https://paxful.com/buy-bitcoin', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0.01, 0], 'trade_market': [0, 0]}}, 'BSQ': {'name': 'Bitsquare', 'color': '800000', 'url': 'https://bitsquare.io/', 'url_book': 'https://market.bitsquare.io/?market=btc_brl', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0, 0], 'out_BTC': [0, 0], 'trade_book': [0, 0.0005], 'trade_market': [0, 0.001]}}, 'BTD': {'name': 'BitcoinTrade', 'color': '000000', 'url': 'https://bitcointrade.com.br/', 'url_book': 'https://bitcointrade.com.br/marketplace', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0099, 4.9], 'out_BTC': [0, 0], 'trade_book': [0.005, 0], 'trade_market': [0.005, 0]}}, 'BZX': {'name': 'Braziliex', 'color': '3cb44b', 'url': 'https://braziliex.com/', 'url_book': 'https://braziliex.com', 'fees': {'in_BRL': [0, 0], 'in_BTC': [0, 0], 'out_BRL': [0.0025, 9], 'out_BTC': [0, 0.001], 'trade_book': [0.005, 0], 'trade_market': [0.005, 0]}}}
orderBookStatsURL = 'https://api.bitvalor.com/v1/order_book_stats.json'
mbtAuth = mbt.Auth(id=credentials.MercadoBitcoin['id'],
                   pin=credentials.MercadoBitcoin['pin'],
                   secret=credentials.MercadoBitcoin['secret'])
foxAuth = fox.Auth(id=credentials.FoxBit['key'],
                   secret=credentials.FoxBit['secret'])
mbtTrade = mbt.Trade(mbtAuth)

## Global variables/configs
# Set this to true to debug all functions and methods (no order will be sent)
debugAll = True
# Set the exchanges in which you want to trade (each one must have its API implemented)
allowedExchanges = ['FOX', 'MBT']
# Set this to the initial BTC ammount to sell
sellingBTCQuantity = 0.0005


def do_taker_market_arbitrage(exchangeInWhichToSell,
                              exchangeInWhichToBuy,
                              priceAtWhichToSell,
                              priceAtWhichToBuy,
                              debug=False):
    '''
    Does the arbitrage by setting:
        a sell market order in exchangeInWhichToSell and
        a buy  market order in exchangeInWhichToBuy,
        in a way in which the same initial BTC selling quantity is obtained in the buying exchange.
    If debug is True, this will NOT send the orders, instead it will print how they'd be have sent.
    '''

    ## These are critical for calculating the orders
    # The fee percentage for selling
    sFee = feesData[exchangeInWhichToSell]['fees']['trade_market'][0]
    # The fee percentage for buying
    bFee = feesData[exchangeInWhichToBuy]['fees']['trade_market'][0]
    # The calculated BTC quantity for making a buy order that gives you the same quantity you sold
    # i.e.: the quantity you sold + fees = gives you same liquid quantity as you initially sold
    buyingBTCQuantity = round(sellingBTCQuantity + (sellingBTCQuantity * (bFee / (1 - bFee))), 8)

    ## These are just for shows (printing information):
    # The calculated total fiat value that you will get while selling
    sellingTotalBRL = format(sellingBTCQuantity * (priceAtWhichToSell - (sFee * priceAtWhichToSell)), '.2f')
    # The calculated total fiat value that you will pay while buying
    buyingTotalBRL = format(buyingBTCQuantity * priceAtWhichToBuy, '.2f')

    ## Places the selling order
    print('Placing ' + format(sellingBTCQuantity, '.8f') + ' BTC sell order in ' + exchangeInWhichToSell + '... (' + sellingTotalBRL + ' BRL)')
    if exchangeInWhichToSell == 'MBT':
        if debug is True:
            print('mbtTrade.place_sell_order(quantity=' + str(sellingBTCQuantity) + ', limit=' + str(priceAtWhichToSell) + ')')
        else:
            mbtOrder = mbtTrade.place_sell_order(quantity=sellingBTCQuantity, limit=priceAtWhichToSell)
            print(mbtOrder.data)
    elif exchangeInWhichToSell == 'FOX':
        if debug is True:
            print('fox.place_sell_order(quantity=' + str(sellingBTCQuantity) + ', limit=' + str(priceAtWhichToSell) + ', auth=foxAuth)')
        else:
            fox.place_sell_order(quantity=sellingBTCQuantity, limit=priceAtWhichToSell, auth=foxAuth)

    ## Places the buying matching order
    print('Placing ' + format(buyingBTCQuantity, '.8f') + ' BTC buy order in ' + exchangeInWhichToBuy + '... (' + buyingTotalBRL + ' BRL)')
    if exchangeInWhichToBuy == 'MBT':
        if debug is True:
            print('mbtOrder = mbtTrade.place_buy_order(quantity=' + str(buyingBTCQuantity) + ', limit=' + str(priceAtWhichToBuy) + ')')
        else:
            mbtOrder = mbtTrade.place_buy_order(quantity=buyingBTCQuantity, limit=priceAtWhichToBuy)
            print(mbtOrder.data)
    elif exchangeInWhichToBuy == 'FOX':
        if debug is True:
            print('fox.place_buy_order(quantity=' + str(buyingBTCQuantity) + ', limit=' + str(priceAtWhichToBuy) + ', auth=foxAuth)')
        else:
            fox.place_buy_order(quantity=buyingBTCQuantity, limit=priceAtWhichToBuy, auth=foxAuth)


def fetch_balances(debug=False):
    '''
    Updates BTC and BRL balance for each exchange in allowedExchanges
    If debug is true, this will return fake balances
    '''

    if debug is True:
        return {'FOX': {'BRL': 300.00774918, 'BTC': 0.00887171}, 'MBT': {'BRL': 244.65601, 'BTC': 0.01129132}}

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


def fetch_orderbooks(debug=False):
    '''
    Fetches order book data from BitValor.
    If debug is true, this will return fake prices with arbitrage opportunity.
    '''

    if debug is True:
        return {'FOX': {'bid': 22100.0313, 'ask': 22200.0001}, 'MBT': {'bid': 24100.2, 'ask': 24200.111022}}

    # Prefills the dict
    returnValue = {e: {'bid': 0, 'ask': 0} for e in allowedExchanges}

    for exchange in allowedExchanges:
        if exchange == "MBT":
            response = requests.get('https://www.mercadobitcoin.net/api/BTC/orderbook/')
            rJSON = response.json()
            returnValue['MBT']['bid'] = rJSON['bids'][0][0]
            returnValue['MBT']['ask'] = rJSON['asks'][0][0]
        elif exchange == "FOX":
            response = requests.get('https://api.blinktrade.com/api/v1/BRL/orderbook?crypto_currency=BTC')
            rJSON = response.json()
            returnValue['FOX']['bid'] = rJSON['bids'][0][0]
            returnValue['FOX']['ask'] = rJSON['asks'][0][0]
        else:
            print('[ERROR] This exchange is not implemented yet.')
            sys.exit()

    return returnValue


## Main Code
def main(debug=False):
    global balances
    exchanges = fetch_orderbooks(debug)

    # Loops through the exchange where you'll buy
    for bExchange, bPrice in exchanges.items():
        for sExchange, sPrice in exchanges.items():
            # Don't compare the exchange against itself
            if bExchange == sExchange:
                continue

            # The fee percentage for selling
            sFee = feesData[sExchange]['fees']['trade_market'][0]
            # The fee percentage for buying
            bFee = feesData[bExchange]['fees']['trade_market'][0]

            # The price people are willing to pay for 1 btc at the market (less the fees):
            totalSPrice = sPrice['bid'] - (sFee * sPrice['bid'])
            # The price people are asking for 1 btc at market (plus the fees):
            totalBPrice = bPrice['ask'] + (bFee * bPrice['ask'])

            # Calculates the profit, if any (including fees)
            profit = ((totalSPrice / totalBPrice) - 1) * 100

            # If the value you'll get for selling 1 BTC is higher to the value you'll pay for 1 BTC (value assumes the fees are embedded)
            # and if the profit is higher than 0.2%, then execute the order
            if (totalSPrice > totalBPrice) and profit > 0:
                print('Arbitrage opportunity (' + format(profit, '.2f') + '%) | ' + time.ctime())
                print('Sell in ' + sExchange + ' at ' + format(sPrice['bid'], '.5f') + '  (-' + format(sFee * 100, '.2f') + '%: ' + format(totalSPrice, '.2f') + ')')
                print('Buy  in ' + bExchange + ' at ' + format(bPrice['ask'], '.5f') + '  (+' + format(bFee * 100, '.2f') + '%: ' + format(totalBPrice, '.2f') + ')')

                # Plays bell sound
                os.system('paplay beep.wav')

                # Does market arbitrage
                # if sExchange == 'MBT':  # for now only do arbitrage if MBT has higher price
                #                         # because i have no btc left in FOX
                do_taker_market_arbitrage(exchangeInWhichToSell=sExchange,
                                          exchangeInWhichToBuy=bExchange,
                                          priceAtWhichToSell=sPrice['bid'],
                                          priceAtWhichToBuy=bPrice['ask'],
                                          debug=debug)
                # Refresh balances
                balances = fetch_balances(debug)
                print("We're done for now, take a look to see if it worked! Balances below: \n")
                pprint(balances)
                #sys.exit()


## The Loop
try:
    # Changes PWD to Arbit dir
    current_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    os.chdir(current_dir)

    # Fetches balances only once at start
    balances = fetch_balances(debugAll)
    pprint(balances)

    while True:
        main(debugAll)
        time.sleep(60)
except KeyboardInterrupt:
    print('\rExiting...')

