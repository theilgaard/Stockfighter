#!/usr/bin/python
import stockfighter
import sys
import os
from time import sleep


if len(sys.argv) != 4:
    print("[!] usage: "+sys.argv[0]+" account venue stock")
    exit(1)

account = sys.argv[1]
venue = sys.argv[2]
symbol = sys.argv[3]

print("[+] Account: " + account)
print("[+] Venue: " + venue)
print("[+] Symbol: " + symbol)

apikey = os.environ.get('sfapi')
if apikey is None:
    print("[!] No API key set, set environment var sfapi!")
    exit(1)
sf = stockfighter.StockFighter(apikey)

order = {
     'account': account,
     'venue': venue,
     'symbol': symbol,
     'price': 5000,
     'qty': 1000,
     'direction': 'buy',
     'orderType': 'limit'
}

goal = 100000
placedorders = 0
orders = []
while placedorders != goal:
    sleep(0.5)
    orderbook = sf.getOrderbook(venue, symbol)
    if orderbook is not None and orderbook['asks'] is not None:
        order['price'] = orderbook['asks'][0]['price']
        print("[+] Placing order at price: " + str(order['price']) + ". Orders: "+str(placedorders)+"/"+str(goal))
        o = sf.placeOrder(order)
        orders.append(o)
        placedorders += order['qty']