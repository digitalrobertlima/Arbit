#!/usr/bin/env python
from pprint import pprint
import credentials
import mbapi.tapi as mbt
#import foxapi.foxbit as fox

mbtAuth = mbt.Auth(id=credentials.MercadoBitcoin['id'],
                   pin=credentials.MercadoBitcoin['pin'],
                   secret=credentials.MercadoBitcoin['secret'])

# foxAuth = fox.Auth(id=credentials.FoxBit['key'],
#                    secret=credentials.FoxBit['secret'])

mbtTrade = mbt.Trade(mbtAuth)

# pprint(fox.get_account_info(foxAuth))


mbtOrder = mbtTrade.place_buy_order(quantity=0.001, limit=12000)
print(mbtOrder.data)


#foxOrder = fox.place_buy_order(limit=12000.002, quantity=0.001, auth=foxAuth)
#fox.cancel_order(1459162516665, foxAuth)

# Exemplo de ordem
#response = mbTrade.place_buy_order(0.001, 22000)  # place a buy order
#pprint(response.data)
#mbTrade.cancel_order(response.data['order']['order_id'])  # cancel the buy order


# ## Código abaixo para substituir bitvalor
# import requests
# response = requests.get('https://www.mercadobitcoin.net/api/BTC/orderbook/')
# rJSON = response.json()
# print(rJSON['bids'][0][0], rJSON['asks'][0][0])

# response = requests.get('https://api.blinktrade.com/api/v1/BRL/orderbook?crypto_currency=BTC')
# rJSON = response.json()
# print(rJSON['bids'][0][0], rJSON['asks'][0][0])