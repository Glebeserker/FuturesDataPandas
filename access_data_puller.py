# In order for the code to work need to run setup.py found in ../TWS API/source/pythonclient
# For set up to run need to have python wheels installed on system 
# Using wheels for IBAPI can be found https://stackoverflow.com/questions/57618117/installing-the-ibapi-package answer 
# Replacing python3 in command line with just python

#importing IBAPI pythonclient components for application


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import *
from contracts import contract_list

#threading and time to control the process of the app and csv to write csv files
import threading
import time
import datetime

import csv
# imported pandas in order to convert dictionary of price to panda and eventually to excel(in progress)
import pandas as pd
from collections import defaultdict

futures_data = defaultdict(list)

#IB constructor class to send and recieve data
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        
    def productDetails(self, reqId):
        if reqId == 0:
            futures_data['Product'].append('VIX AUG')
            futures_data['Datestamp'].append(datetime.datetime.now("%Y%m%d"))
            futures_data['Timestamp'].append(datetime.datetime.now("%X"))
            futures_data['Exparation Date'].append(20210818)
            
    def tickPrice(self, reqId, tickType, price, attrib):
        
        
        # ask price if statement for each month
        if tickType == 67: 
            
            if reqId == 1:
                print('July ask price is: ', price)
                futures_data['Ask Price'].append(price)
                
            elif reqId == 2:
                print('August ask price is: ', price)
                futures_data['Ask Price'].append(price)
                
            elif reqId == 3: 
                print('September ask price is: ', price)
                futures_data['Ask Price'].append(price)
                
            elif reqId == 4:
                print('Ocotber ask price is: ', price)
                futures_data['Ask Price'].append(price)
            else: 
                print('Incorrect reqId') 
    
        elif tickType == 68: 
            
            if reqId == 1:
                print('July last price was: ', price)
                
                futures_data['Last Price'].append(price)
            elif reqId == 2:
                print('August last price was: ', price)
                futures_data['Last Price'].append(price)
            elif reqId == 3:
                print('September last price was: ', price)
                futures_data['Last Price'].append(price)
            elif reqId == 4:
                print('Ocotber last price was: ', price)
                futures_data['Last Price'].append(price)
            else:
                print('Incorrect reqId')
                

        elif tickType == 66: 
            
            if reqId == 1:
                print('July bid price is: ', price)
                
                futures_data['Bid Price'].append(price)
            elif reqId == 2:
                print('August bid price is: ', price)
                futures_data['Bid Price'].append(price)
            elif reqId == 3:
                print('September bid price is: ', price)
                futures_data['Bid Price'].append(price)
            elif reqId == 4:
                print('October bid price is: ', price)
                futures_data['Bid Price'].append(price)
            else:
                print('Incorrect reqId')
        
        
        
    # function to call size parameters of things
    def tickSize(self, reqId, tickType, size):
        
        if tickType == 69: 
            
            if reqId == 1:
                print("July bid size is: ",size)
                
                futures_data['Bid Size'].append(size)
            elif reqId == 2:
                print('August bid size is: ', size)
                futures_data['Bid Size'].append(size)
            elif reqId == 3:
                print('September bid size is: ', size)
                futures_data['Bid Size'].append(size)
            elif reqId == 4:
                print('October bid size is: ', size)
                futures_data['Bid Size'].append(size)
            else: 
                print('Incorrect reqId')
                
            
        elif tickType == 70:
            
            if reqId == 1:
                print('July ask size is: ', size)
                futures_data['AskSize'].append(size)
            elif reqId == 2:
                print('August ask size is: ', size)
                futures_data['AskSize'].append(size)
            elif reqId == 3:
                print('September ask size is: ', size)
                futures_data['AskSize'].append(size)
            elif reqId == 4:
                print('October ask size is: ', size)
                futures_data['AskSize'].append(size)
            else:
                print('Incorrect reqId')
                  
        elif tickType == 74:
            
            if reqId == 1:
                print('July volume is: ', size)
                
                futures_data['Volume'].append(size)
            elif reqId == 2:
                print('August volume is: ', size)
                futures_data['Volume'].append(size)
            elif reqId == 3:
                print('September volume is: ', size)
                futures_data['Volume'].append(size)
            elif reqId == 4:
                print('October volume is: ', size)
                futures_data['Volume'].append(size)
                
        elif tickType == 71:
            
            if reqId == 1:
                print('July last size was: ', size)
                
                futures_data['Last Size'].append(size)
            elif reqId == 2:
                print('August last size was: ', size)
                futures_data['Last Size'].append(size)
            elif reqId == 3:
                print('September last size was: ', size)
                futures_data['Last Size'].append(size)
            elif reqId == 4:
                print('October last size was: ', size)
                futures_data['Last Size'].append(size)    
                
    def nextValidId(self, orderId:int):
        self.nextOrderId = orderId
        print(orderId)
      
       

       
                

def run_loop():
	app.run()
# calling up IBAPI class instance and connecting the app to local host server
app = IBapi()
app.connect('127.0.0.1', 7497, 136)
app.nextOrderId = 0


#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server


        



# 1) Live Data
# 2) Frozen
# 3) Delayed
# 4) Delayed Frozen
#Request Market Data as 3 = Delayed since using paper account at the moment 
app.reqMarketDataType(3)

#app.placeOrder(IBapi.nextValidId, july_vixFuture_contract, july_order)
# Requesting Market Data for Euro to Usd ask price 1 = unique identifier, contract info, string for genericTickList (https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#a7a19258a3a2087c07c1c57b93f659b63)
# boolean value if want a one-time snap shot, boolean value for regulatory snapshot, [] = mktDataOptions TagValue.

app.reqMktData(1, contract_list[0], '', False, False, [])
app.reqMktData(2, contract_list[1], '', False, False, [])
app.reqMktData(3, contract_list[2], '', False, False, [])
app.reqMktData(4, contract_list[3], '', False, False, [])




time.sleep(1) #Sleep interval to allow time for incoming price data
print(futures_data)
time.sleep(2)
futdt = pd.DataFrame.from_dict(futures_data, orient='columns', dtype=None, columns=None)
print(futdt)
# Calling disconnect, otherwise the infinite loop occurs
app.disconnect()
