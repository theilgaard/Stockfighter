import httplib2
import json

class StockFighter:
    def __init__(self, apikey):
        self.orders = {}
        self.headers = {'X-Starfighter-Authorization':apikey}
        self.http = httplib2.Http(".cache")

    def isApiUp(self):
        url = "https://api.stockfighter.io/ob/api/heartbeat"
        (resp_headers, content) = self.http.request(url, "GET")
        health = json.loads(content.decode('UTF-8'))
        return health['ok']

    def isVenueUp(self, venue):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/heartbeat"
        (resp_headers, content) = self.http.request(url, "GET")
        health = json.loads(content.decode('UTF-8'))
        return health['ok']

    def stockOnVenue(self, venue):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks"
        (resp_headers, content) = self.http.request(url, "GET")
        stocks = json.loads(content.decode('UTF-8'))
        if stocks['ok']:
            return stocks['symbols']
        else:
            print("[!] Error retrieving stocks on venue: " + stocks['error'])

    def getOrderbook(self, venue, stock):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock 
        (resp_headers, content) = self.http.request(url, "GET")
        orderbook = json.loads(content.decode('UTF-8'))
        if orderbook['ok']:
            return orderbook
        else:
            print("[!] Error retrieving orderbook: " + orderbook['error'])

    def placeOrder(self, order):
        url = "https://api.stockfighter.io/ob/api/venues/"+order['venue']+"/stocks/"+order['symbol']+"/orders"
        (resp_headers, content) = self.http.request(url, "POST", headers=self.headers, body=json.dumps(order))
        orderreply = json.loads(content.decode('UTF-8'))
        if orderreply['ok']:
            print("[+] Placed {} order [id: {} @ {}:{}] [Price: {}$] [Filled: {}/{}]".format(
                    orderreply['direction'],
                    orderreply['id'],
                    order['venue'],
                    order['symbol'],
                    order['price'] / 100,
                    orderreply['totalFilled'],
                    order['qty']
                ))
            self.orders[orderreply['id']] = orderreply
            return orderreply
        else: 
            print("[!] Error placing order: " + orderreply['error'])

    def getQuote(self, venue, stock):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock+"/quote"
        (resp_headers, content) = self.http.request(url, "GET")
        quote = json.loads(content.decode('UTF-8'))
        if quote['ok']:
            return quote
        else:
            print("[!] Error retrieving quote for stock: " + quote['error'])

    def getOrderStatus(self, venue, stock, orderid):
        url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+orderid
        (resp_headers, content) = self.http.request(url, "GET")
        status = json.loads(content.decode('UTF-8'))
        if status['ok']:
            return status
        else:
            print("[!] Error retrieving status for order: " + status['error'])

    def cancelOrder(self, venue, stock, order):
        if order is not None:
            url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+str(order['id'])
            (resp_headers, content) = self.http.request(url, "DELETE", headers=self.headers)
            response = json.loads(content.decode('UTF-8'))
            if response['ok']:
                print("[+] Cancelled order: " + str(order['id']))
                self.orders[order['id']] = None
                return response
            else:
                print("[!] Error cancelling order: " + response['error'])

    def getOrders(self, venue, account, stock=None):
        url = ''
        if stock is None:
            url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/accounts/"+account+"/orders"
        else:
            url = "https://api.stockfighter.io/ob/api/venues/"+venue+"/accounts/"+account+"/stocks/"+stock+"/orders"
        (resp_headers, content) = self.http.request(url, "GET", headers=self.headers)
        orders = json.loads(content.decode('UTF-8'))
        if orders['ok']:
            return orders
        else:
            print("[!] Error retrieving orders: " + orders['error'])

    def getQuoteSpread(self, quote):
        if quote is not None:
            if 'ask' not in quote:
                print("[!] 'ask' not in quote")
                return -1
            if 'bid' not in quote:
                print("[!] 'bid' not in quote")
                return -2
            return quote['ask'] - quote['bid']
        else:
            print("[!] Quote was None")
            return -1

    def getSpread(self, orderbook):
        if orderbook is None:
            print("[!] Orderbook was None")
            return -1
        asks = orderbook['asks']
        bids = orderbook['bids']
        if asks is None:
            print("[!] 'asks' was None")
            return -2
        if bids is None:
            print("[!] 'bids' was None")
            return -3
        return asks[0] - bids[0]