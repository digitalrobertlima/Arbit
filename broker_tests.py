#!/usr/bin/env python
import credentials
from pprint import pprint
import mbapi.tapi as mbt
import foxapi.foxbit as fox

mbtAuth = mbt.Auth(id=credentials.MercadoBitcoin['id'],
                   pin=credentials.MercadoBitcoin['pin'],
                   secret=credentials.MercadoBitcoin['secret'])

foxAuth = fox.Auth(id=credentials.FoxBit['key'],
                   secret=credentials.FoxBit['secret'])

mbTrade = mbt.Trade(mbtAuth)
pprint(mbTrade.list_orders().data)

pprint(fox.list_orders(foxAuth))

# Exemplo de ordem
#response = mbTrade.place_buy_order(0.001, 22000)  # place a buy order
#pprint(response.data)
#mbTrade.cancel_order(response.data['order']['order_id'])  # cancel the buy order
