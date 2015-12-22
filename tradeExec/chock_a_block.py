#!/usr/bin/python
import httplib2
import configparser
import os.path
import os
import pprint

cfgFile = "tradeExec.cfg"
if os.path.isfile(cfgFile):
    config = configparser.RawConfigParser()
    config.read(cfgFile)
    print("[+] Config loaded: " + cfgFile)
else:
    print("[!] Config file not found: " + cfgFile)
    exit(1)

apikey = os.environ.get('STOCKAPIKEY')
if apikey is not None:
    print("[+] API Key: " + apikey)
else:
    print("[!] API Key not set")
    exit(1)

baseurl = config.get('Stockfighter', 'baseurl')

order = {
    'account': config.get('Chock a block', 'account'),
    'venue': config.get('Chock a block', 'venue'),
    'symbol': config.get('Chock a block', 'symbol'),
    'price': config.get('Chock a block', 'price'),
    'qty': 100,
    'direction': 'buy',
    'orderType': 'limit'
}

print('[+] Base URL: ' + baseurl)
print('[+] Account: ' + order['account'])
print('[+] Venue: ' + order['venue'])
print('[+] Symbol: ' + order['symbol'])

urlstocks = baseurl + "/venues/" + order['venue'] + "/stocks"
url = baseurl + "/venues/" + order['venue'] + "/stocks/" + order['symbol'] + "/orders"

h = httplib2.Http(".cache")
(resp_headers, content) = h.request(urlstocks, "GET",
                                    headers={'X-Starfighter-Authorization':apikey})


pprint.pprint(content)
