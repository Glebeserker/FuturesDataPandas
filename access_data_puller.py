from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from contracts import contract_list
import pandas as pd
import datetime
from collections import defaultdict

import threading
import time

futures_data = defaultdict(list)



class dataPull( EWrapper):
    def nextValidId(self, orderId: int):
       print(orderId)
       self.start()
    def productDetails(self, reqId):
        if reqId == 0:
            futures_data['Product'].append('VIX AUG')
            futures_data['Datestamp'].append(datetime.datetime.now("%Y%m%d"))
            futures_data['Timestamp'].append(datetime.datetime.now("%X"))
            futures_data['Exparation Date'].append(20210818)
            
        
    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 66:
            if reqId ==0:
                futures_data['Bid Price'].append(price)
            
        elif tickType == 67:
            if reqId ==0:
                futures_data['Ask Price'].append(price)
        
        elif tickType == 68:
            if reqId ==0:
                futures_data['Last Price'].append(price)
            
    def tickSize(self, reqId, tickType, size):
        if tickType == 69:
            if reqId ==0:
                futures_data['Bid Size'].append(size)
        
        elif tickType == 70:
            if reqId ==0:
                futures_data['AskSize'].append(size)
            
        elif tickType == 74:
            if reqId ==0:
                futures_data['Volume'].append(size)
            
        elif tickType == 71:
            if reqId ==0:
                futures_data['Last Size'].append(size)
                
    def start(self):
        app.reqMarketDataType(3)
        app.reqMktData(0, contract_list[1], '', False, False, [])
            

app = EClient(dataPull())
app.connect('127.0.0.1', 7497, 136)
app.run()
    
    
futdt = pd.DataFrame.from_dict(futures_data, orient='columns', dtype=None, columns=None)
print(futdt)

    
app.disconnect
    




