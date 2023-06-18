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