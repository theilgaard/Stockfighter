#!/usr/bin/python3

import stockfighter
import sys
import pprint
import os

apikey = os.environ.get('sfapi')
if apikey is None:
    print("[!] No API key set, set sfapi!")
    exit(1)
sf = stockfighter.StockFighter(apikey)

account = 'BAS79106125'
symbol = 'USEH'
venue = 'LOGEX'

order = {
     'account': account,
     'venue': venue,
     'symbol': symbol,
     'price': int(sys.argv[1]), 
     'qty': 100,
     'direction': 'buy',
     'orderType': 'limit'
}

order = sf.placeOrder(order)
pprint.pprint(order)
