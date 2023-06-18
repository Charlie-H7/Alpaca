import config
import requests
import websockets
import vectorbt as vbt
from datetime import datetime
from datetime import timedelta
from alpaca.trading.client import TradingClient #
from alpaca.trading.requests import MarketOrderRequest  #
from alpaca.trading.enums import OrderSide, TimeInForce #
import alpaca_trade_api as trade_api
import pandas as pd
import pandas_ta
import ccxt

#make stock class in a seperate file so that i can reuse definitions else in this file thus abstracting the Stocks class

API_KEY = 'PKC5JD954B1VO5JIAP6X'
SECRET_KEY = '7vTpqM1mgRhSXBtDaDR9ZcOWLOyUAItPxsPbffHW'
trading_client = TradingClient(API_KEY,SECRET_KEY, paper=True)
api = trade_api.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

account = trading_client.get_account()
temp_1 = api.get_position('PEP')

symbols = []

foo = 0


while datetime.now.hour != 4 :  #ideally i want to stop when there is nothing left to trade, but since running at the same time
    for stock in symbols :
        

        #trading data

        #case 1: the current I dont have a neg pl and support still being approached
        #Breakout above [Hold]
        if curr_price > stock.resistance :
            stock.support = stock.resistance
            stock.resistance = curr_price

        #Case 2: breakout below (Update)
        if curr_price < stock.support :
            stock.resistance = stock.support
            stock.support = curr_price

        #Case 3: Cut loses
        #if stock pos gotten from updating get_pos in the stock loop
        #if cost_basis is 7(X) percent lower than market_price
        #SELL