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

    def placeOrder(self, order):
        url = "https://api.stockfighter.io/ob/api/venues/"+order['venue']+"/stocks/"+order['symbol']+"/orders"
        (resp_headers, content) = self.h.request(url, "POST", self.headers)
        order = json.loads(content.decode('UTF-8'))
        if order['ok']:
            return order
        else: 
            print("[!] Error placing order: " + order['error'])

    def getQuote(self, venue, stock):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock+"/quote"
        (resp_headers, content) = self.h.request(url, "GET")
        quote = json.loads(content.decode('UTF-8'))
        if quote['ok']:
            return quote
        else:
            print("[!] Error retrieving quote for stock: " + quote['error'])

    def getOrderStatus(self, venue, stock, orderid):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+orderid
        (resp_headers, content) = self.h.request(url, "GET")
        status = json.loads(content.decode('UTF-8'))
        if status['ok']:
            return status
        else:
            print("[!] Error retrieving status for order: " + status['error'])

    def cancelOrder(self, venue, stock, orderid):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+orderid
        (resp_headers, content) = self.h.request(url, "DELETE", self.headers)
        response = json.loads(content.decode('UTF-8'))
        if response['ok']:
            return response
        else:
            print("[!] Error cancelling order: " + response['error'])

    def getOrders(self, venue, account, stock=None):
        url = ''
        if stock is None:
            url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/accounts/"+account+"/orders"
        else:
            url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/accounts/"+account+"/stocks/"+stock+"/orders"
        (resp_headers, content) = self.h.request(url, "GET", self.headers)
        orders = json.loads(content.decode('UTF-8'))
        if orders['ok']:
            return orders
        else:
            print("[!] Error retrieving orders: " + orders['error'])

