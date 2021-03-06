# use of the Trades{..} classes
import json
import requests
from oandapyV20 import API


import oandapyV20.endpoints.trades as trades
import sys

access_token = "b2aa44b8e9a8c723097aa05c84f0e6ae-867bd81043a7928fad38c5b53e0d548b"
accountID = "sv768593"

api = API(access_token=access_token)
chc=sys.argv[1]

if chc == 'list':
   r = trades.TradesList(accountID)
   rv = api.request(r)
   print("RESP:\n{} ".format(json.dumps(rv, indent=2)))

if chc == 'open':
   r = trades.OpenTrades(accountID)
   rv = api.request(r)
   print("RESP:\n{} ".format(json.dumps(rv, indent=2)))
   tradeIDs = [o["id"] for o in rv["trades"]]
   print("TRADE IDS: {}".format(tradeIDs))

if chc == 'details':
   for O in sys.argv[2:]:
       r = trades.TradeDetails(accountID, tradeID=O)
       rv = api.request(r)
       print("RESP:\n{} ".format(json.dumps(rv, indent=2)))

if chc == 'close':
   X = iter(sys.argv[2:])
   for O in X:
       cfg = { "units": X.next() }
       r = trades.TradeClose(accountID, tradeID=O, data=cfg)
       rv = api.request(r)
       print("RESP:\n{} ".format(json.dumps(rv, indent=2)))

if chc == 'cltext':
   for O in sys.argv[2:]:  # tradeIDs
       cfg = { "clientExtensions": {
               "id": "myID{}".format(O),
               "comment": "myComment",
            }
         }
       r = trades.TradeClientExtensions(accountID, tradeID=O, data=cfg)
       rv = api.request(r)
       print("RESP:\n{} ".format(json.dumps(rv, indent=2)))

if chc == 'crc_do':
   X = iter(sys.argv[2:])
   for O in X:
       cfg = {
               "takeProfit": {
                 "timeInForce": "GTC",
                 "price": X.next(),
               },
               "stopLoss": {
                 "timeInForce": "GTC",
                 "price": X.next()
               }
         }
       r = trades.TradeCRCDO(accountID, tradeID=O, data=cfg)
       rv = api.request(r)
       print("RESP:\n{} ".format(json.dumps(rv, indent=2)))