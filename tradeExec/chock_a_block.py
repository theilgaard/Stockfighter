#!/usr/bin/python
import httplib2
import configparser
import os.path
import os

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
venue = config.get('Chock a block', 'venue')
symbol = config.get('Chock a block', 'symbol')
account = config.get('Chock a block', 'account')

print('[+] Base URL: ' + baseurl)
print('[+] Account: ' + account)
print('[+] Venue: ' + venue)
print('[+] Symbol: ' + symbol)

#h = httplib2.Http(".cache")
#(resp_headers, content) = h.request("http://dr.dk", "GET")

#print(content)
