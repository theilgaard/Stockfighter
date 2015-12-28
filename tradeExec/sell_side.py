#!/usr/bin/python3
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

# ========================
# 

order = {
     'account': account,
     'venue': venue,
     'symbol': symbol,
     'price': 5000,
     'qty': 100,
     'direction': 'buy', # buy or sell
     'orderType': 'limit'
}

maxorders = 1000
previousBid = None
previousAsk = None
spread = -1

def checkBid(quote):
	global previousBid
	currentBid = quote['bid']
	if currentBid is not None:
		if previousBid is not None and previousBid['price'] == currentBid:
			pass # We're in the lead
		else:
			order['price'] = currentBid + 1
			order['direction'] = 'buy'
			orderreply = sf.placeOrder(order)
			sf.cancelOrder(venue, symbol, previousBid)
			previousBid = orderreply

def checkAsk(quote):
	global previousAsk
	currentAsk = quote['ask']
	if currentAsk is not None:
		if  previousAsk is not None and previousAsk['price'] == currentAsk:
			pass # We're in the lead
		else:
			order['price'] = currentAsk - 1
			order['direction'] = 'sell'
			orderreply = sf.placeOrder(order)
			sf.cancelOrder(venue, symbol, previousAsk)
			previousAsk = orderreply
			

while True:
	sleep(0.1)
	if len(sf.orders) < maxorders:
		quote = sf.getQuote(venue, symbol)
		spread = sf.getQuoteSpread(quote)
		print("[*] Spread: " + str(spread))
		if spread > 2:
			checkBid(quote)
			checkAsk(quote)
