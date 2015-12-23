import httplib2
import json

class StockFighter:
    def __init__(self, apikey):
        self.headers = {'X-Starfighter-Authorization':apikey}
        self.h = httplib2.Http(".cache")

    def isApiUp(self):
        url = "https://api.stockfighter.io/ob/api/heartbeat"
        (resp_headers, content) = self.h.request(url, "GET")
        health = json.loads(content.decode('UTF-8'))
        return health['ok']

    def isVenueUp(self, venue):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/heartbeat"
        (resp_headers, content) = self.h.request(url, "GET")
        health = json.loads(content.decode('UTF-8'))
        return health['ok']

    def stockOnVenue(self, venue):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks"
        (resp_headers, content) = self.h.request(url, "GET")
        stocks = json.loads(content.decode('UTF-8'))
        if stocks['ok']:
            return stocks['symbols']
        else:
            print("[!] Error retrieving stocks on venue: " + stocks['error'])

    def getOrderbook(self, venue, stock):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock 
        (resp_headers, content) = self.h.request(url, "GET")
        orderbook = json.loads(content.decode('UTF-8'))
        if orderbook['ok']:
            return orderbook
        else:
            print("[!] Error retrieving orderbook: " + orderbook['error'])

