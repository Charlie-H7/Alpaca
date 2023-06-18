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



#Ideally I would like to allocate a higher percentage of the available funds to buy more potential yield/higher current price

class Stocks :
    def __init__(self, symbol, resistance, support):
        self.symbol = symbol
        self.resistance = resistance
        self.support = support
    
    def log_curr_price(self, value) :
        self.curr_price = value

    def update_allocations(self, total_price) :
        self.allocation = self.curr_price / total_price
            
    #def buying_funds(self):
     #   buying_power = account.buying_power
         

        #this limits the way allocation need to weigh them instead
        """
        #allocate funds to distribute based on how much the stock is worth
        curr_price = api.get_latest_quote(self.symbol)

        if curr_price < 50 :
            self.allocation = .1
        if curr_price < 200 :
            self.allocation = .25
            """
        
            
        

API_KEY = 'PKC5JD954B1VO5JIAP6X'
SECRET_KEY = '7vTpqM1mgRhSXBtDaDR9ZcOWLOyUAItPxsPbffHW'
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
api = trade_api.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

#positions = trading_client.get_all_positions() Pos is for live
account = trading_client.get_account()
buying_power = account.buying_power   #CHECK IF MEMBER OR DEF (FUNCTION OR MEMBER) EIOSAKHJBDFEIHVSEJH


dev_perc = 0.05    #Used for live
#this contains the list of symbol string im interested in purchasing
symbols = []
file = open("supres.txt", 'r')
junk_line = file.readline()
text = file.read()
words = text.split()

#Preprocess data: Checks support and res from a file generated by 'marketdata.py'
for i in range(0, len(words), 3) : #step size 3 because of num cols
    symbols.append(Stocks(words[i],float(words[i+1]),float(words[i+2])))


# Determine the funds to allocate
total_price = 0
for stock in symbols :
    quote = api.get_latest_quote(stock.symbol)
    curr_price = float(quote.ask_price)    #ask price, CAN BE SUBBED OUT WITH 'get_last_trade'
    total_price += curr_price      #price of stock in stocks
    stock.log_curr_price(curr_price)
    

#Allocated funds, price weighted allocation
for stock in symbols : 
    stock.update_allocations(total_price)



#forever we want to check each stock and update
while datetime.now().hour != 4 or buying_power <  1 : #tk

    #Check for any breakouts, or within buying range
    for stock in symbols :
        quote = api.get_latest_quote(stock.symbol)
        latest_quote = float(quote.ask_price)
        
        #---Cases---#

        #Case 1
        #Breakout below - Triggers when strictly below support  TYPICALLY WOULD CHECK IF STILL IN DOWNTREND
        if latest_quote < (stock.support - (stock.support * dev_perc)) : #while is support and is uptrend, just for after above breakout is made   


            #BUY
            stock.resistance = stock.support
            stock.support = latest_quote
            #Request
            market_order_data = MarketOrderRequest(
                                symbol = stock.symbol,
                                qty = stock.allocation / latest_quote,
                                side = OrderSide.BUY,
                                time_in_force = TimeInForce.DAY
                                )
            trading_client.submit_order(market_order_data)

        #Case 2
        #Breakout above - Triggers when strictly above resistance   [Hold]
        elif latest_quote > stock.resistance :
            stock.support = stock.resistance
            stock.resistance = latest_quote

        #Case 3
        #Buy above or below by dev when no breakout and current price close to support  {maybe 1st and cond will lead to issues since may pay for high price dev check on paper}
        else :
            #if curr_price closer to support line buy
            if (stock.resistance - latest_quote > latest_quote - stock.support) and ((stock.support + (stock.support * dev_perc) > latest_quote) or ((stock.support - (stock.support * dev_perc)) < latest_quote)) :
                #Buy
                #Request
                market_order_data = MarketOrderRequest(
                                    symbol = stock.symbol,
                                    qty = stock.allocation / latest_quote,
                                    side = OrderSide.BUY,
                                    time_in_force = TimeInForce.DAY
                                    )
                trading_client.submit_order(market_order_data)





