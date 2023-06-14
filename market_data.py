import requests
import websockets
import vectorbt as vbt
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit
from datetime import timedelta
from alpaca.trading.client import TradingClient #
from alpaca.trading.requests import MarketOrderRequest  #
from alpaca.trading.enums import OrderSide, TimeInForce #
import alpaca_trade_api as trade_api
import pandas as pd
import pandas_ta
import ccxt


#In summary, 
#1. Return a get_bars().df      [NOTE .DF]
#2 the return of get_bars().df is a dataframe such that we can index into right data with the symbol        [like a spreadsheet]
    # -> Symbols are like rows and cold are what we index into
#3


API_KEY = 'PKC5JD954B1VO5JIAP6X'
SECRET_KEY = '7vTpqM1mgRhSXBtDaDR9ZcOWLOyUAItPxsPbffHW'
api = trade_api.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')


#Get_barset is no longer useful ****
#The adjustment parameter allows you to specify how the historical data should be adjusted. It can take the following values:
#'raw': Returns the raw unadjusted historical data.
#symbol = 'AAPL'  # Trading symbol for Apple Inc.
symbol = ['AAPL', 'PEP']


# Calculate the start and end dates
end_range = datetime.now().date() - timedelta(days=1) # Yesterday date, (since i cant query into past 15 mins :'v[just track myself])
start_range = end_range - timedelta(days=14)  # 2 weeks ago

datetime.weekday
#today = datetime.now().date()

#start_range = timedelta(13) #get the time from 2 weeks ago (date)
#end_range = timedelta(1) # get today date


bars = api.get_bars(symbol,  '1D' , "2023-05-11", "2023-05-25", adjustment='raw').df
#bars = api.get_bars(symbol,  '1D' , start_range, end_range, adjustment='raw').df



print(bars)

file = open("supres.txt","a")
file.write("Symbol      Resistance       Support\n")

# Extract the high and low columns as variables
high_prices = bars['high']
low_prices = bars['low']
day = 0
support = 0
resistance = 0
curr_high = 0
curr_low = 0
is_init = False
#dev_perc = 0.07    Used for live
symbol_idx = 0


#pair the entries in the df into a pair, where for loop goes from start range : end range
day_hl = zip(high_prices,low_prices)

# Print the high and low prices
print("High Prices:")
for hl in day_hl :      #[apple, pepsico] prints in that order
    print(day)

    if is_init == False :
        print('init sup')
        resistance = hl[0]
        support = hl[1]
        print(support)  #172.17
        is_init = True

    #Check for if there is a breakout of the support or resistance (between) days
    else : #not first day (start range)
        
        curr_high = hl[0]
        curr_low = hl[1]

        #The following cases are to follow the support and resistant trends made by the past 2 week data
        #   Note: This implementation builds support and resistant lines around the high and lows over the day timestamp
        #         Normally one would change both the support and resistance line at a breakout however since we do                  "DELETE"
        #         In the case with multiple breakouts we must guess which breakout occurs first as we cannot tell with the current timestamp of "1D" selected

        #Case where there is multiple possible breakouts in a day
        if curr_high > resistance and curr_low < support :
            #Prioritizes setting the support and resistance based on the highest dif with hl and sup/res
            if curr_high - resistance > support - curr_low : #Breakout above
                support = resistance  # = high??
                resistance = curr_high

            else : #Breakout below
                resistance = support  # = low??
                support = curr_low

        #Breakout above
        elif curr_high > resistance or curr_low > resistance :
            support = resistance
            resistance = curr_high

        #Breakout below
        elif curr_low < support or curr_high < support :
            resistance = support
            support = curr_low

        else :
            print("ERROR: DDEBUG IS CASE")

    day += 1
    #check if a new stock to track
    #Condition is for every 11 days as the market is closed every weekend thus we are only interested in the 15 days (0 indexed from start_range) to end range - 4 weekend days
    if day == 11 :
        day = 0
        is_init = False #resets on a per stock basis if there is a baseline for the 
        #Write to file the support and resistance of each stock over the alloted timeframe

        file.writelines(f"{symbol[symbol_idx]}:        {resistance}             {support}\n")

        #change to the next symbol to print
        symbol_idx += 1
    

"OK; problem - when running through this, i figured that I can loop and access the corresponding high_price with the above code however it does not show the name of the corresponding stock"
"Solution; Since i plan to do small frame trading, I know how many DAYS are done in each barset per symbol in symbols, thus i know what symbol im in by, checking if after n time frime days"

#start: 2023-05-11
#end: 2023-05-25

#asume that there is the correct support and res, print out to a file










#Loop over the rows in our dataframe going in order of the list inserted
# Iterate through the list and df simultaneously
#item = list, data == df
#for item, row in zip(symbol, bars.iterrows()):
 #   index, data = row
  #  high_prices = data['high']

   # print(f"Item: {item}, Highest price: {high_prices}")





#ACCESSING THE DATAFRAME FOR A HIGH/LOW YIELDS A NUMBER THAT CAN BE STORED
#high_prices += 2    #make 2 a float 64     WORKS
#print(high_prices) #High prices stores the data as some sort of object such that when it gets printed other get printed


#HIGH PRICE DDEBUG = 128.46



#want curr day - data from 2 weeks


#The get_bars() method in the Alpaca API returns a BarSet object, which is a dictionary-like object that contains multiple bars for different 
#symbols. To access the individual bars for a specific symbol, you can use the symbol as the key to retrieve the corresponding Bar object.


#THIS IS IMPORTANT ITS ALREADY A DATA FRAME GET BARS()
#'DataFrame' object has no attribute 'df'
#bar_data = bars.df



"""

# Iterate over the bars and access timestamp and bar data
for bar in bars[symbol]:
    print("Timestamp:", bar.t)
    print("Open:", bar.o)
    print("High:", bar.h)
    print("Low:", bar.l)
    print("Close:", bar.c)
    print("Volume:", bar.v)
    print("")

    """

"""
for value, bar in bars.items :
    print(bar)
    print(value)

    #print(value)
    """


 

#bars = api.get_bars("PEP", '1D', start_range, end_range)

#print(bars)

# Save the DataFrame to a CSV file
#bars.to_csv('output.csv', index=False)

#["BTC/USD",'AAPL','PEP']
#TimeFrame.Hour


#Problem if there is a gap i could note where the shit is