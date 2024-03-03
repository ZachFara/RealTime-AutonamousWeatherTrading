import numpy as np
import pandas as pd

class PnLBook:
    """
    This class will be used to keep track of the trades that we make, the assests that we have and then at the end we will calculate the returns that we made.
    It should be able to track the performance of any trading strategy that we implement.
    """

    def __init__(self, verbose = 0):
        self.trades = [] # This will hold the trades that we make. We will later use these to calculate the average return and the standard deviation of the returns
        self.assets = {"Money": 10_000} # This will be our account basically which will hold the total assets of our trader
        self.order_id = 1 # This will be the unique identifier for each trade
        self.open_orders = {} # This will hold the open orders that we have. We will use this to match the sell orders with the buy orders
        self.verbose = verbose

    def buy(self, symbol, price, amount=1):
        """
        This function will be used to buy a stock. It will take in the symbol of the stock, the price at which we are buying the stock and the amount of stock that we are buying.
        It will then update all of the necessary data structures to reflect the new trade that we have made including the open orders dictionary, the assets dictionary and the trades list.
        """

        # We can only buy if we have enough money to buy the stock, otherwise do nothing
        if self.assets["Money"] > price * amount:

            ## Let's open a trade within our list, and within the open orders dictionary ##

            # Open the trade within the list
            trade = {
                "Order ID": self.order_id,
                "Symbol": symbol,
                "Buy Price": price,
                "Sell Price": None,
                "Return": None
            }
            self.trades.append(trade)

            # Now open in the dictionary
            self.open_orders[symbol] = self.order_id

            # Now increment the order id so that we can have a unique identifier for each buy/trade pair
            self.order_id += 1

            # Now let's update the assets, update or instantiate the symbol in the assets dictionary
            if symbol in self.assets:
                self.assets[symbol] += amount
            else:
                self.assets[symbol] = amount
            self.assets["Money"] -= price * amount

            if self.verbose:
                print(f"Order ID: {trade['Order ID']}, Symbol: {trade['Symbol']}, Buy Price: {trade['Buy Price']}, Amount: {amount}")

        else:
            pass 

    def sell(self, symbol, price, amount=1, order_id=None):
        """
        This function will be used to sell a stock. It will intake the symbol of the stock, the price at which we are selling the stock and the amount of stock that we are selling.
        It will then update all of the necessary data structures to reflect the new trade that we have made including the open orders dictionary, the assets dictionary and the trades list.
        It will use the symbol and the open orders dictionary to match the sell order with the buy order. Then it will calculate the return that we made on the trade and update the assets dictionary.
        """

        # Check if we have the asset and if we have enough of it to fulfill the order
        if symbol in self.assets and self.assets[symbol] >= amount:

            # If we don't have the order id, then we will use the open orders dictionary to get the order id
            if order_id is None:
                order_id = self.open_orders[symbol]

            # Now we will find the trade in the trades list and update the sell price and the return
            for trade in self.trades:

                # If we find the trade, then we will update the sell price and the return then break out of the loop
                if trade["Order ID"] == order_id:
                    trade["Sell Price"] = price
                    trade["Return"] = (price - trade["Buy Price"]) * amount
                    if symbol in self.assets:
                        self.assets[symbol] -= amount
                    break

            # If our for loop didn't break, then we didn't find the trade and we should raise an error
            else:
                raise ValueError("Order ID not found")
            
            # Update the assets dictionary with the money that we made from the sale
            self.assets["Money"] += price * amount

            if self.verbose:
                print(f"Order ID: {order_id}, Symbol: {symbol}, Sell Price: {price}, Amount: {amount}")
                
        else:
            pass

    def calculate_total_return(self):
        """
        This function will calculate the total return that we made on all of the trades that we have made. It will iterate through the trades list and sum up all of the returns.
        However, if it finds a trade that we never closed then it will raise an error.
        """

        total_return = 0
        for trade in self.trades:
            if trade["Return"] is not None:
                total_return += trade["Return"]
            else:
                raise ValueError("Trade not closed")
        return total_return
    
    def display_assets(self):
        """
        This function shows the current assets of the trader
        """
        return self.assets
    
    def calculate_sharpe_ratio(self, risk_free_rate):
        """
        This function calculates the sharpe ratio of the trades that we have made. It will use the returns that we have made in the trade list to calculate the sharpre ratio.
        """

        # First we will get all of the returns from the trades list
        returns = [trade["Return"] for trade in self.trades if trade["Return"] is not None]
        
        # Now we will calculate the average return and the standard deviation of the returns
        avg_return = np.mean(returns)
        std_return = np.std(returns)

        # Now we will calculate the sharpe ratio
        sharpe_ratio = (avg_return - risk_free_rate) / std_return
        
        return sharpe_ratio
    
    def current_asset_value(self, prices):
        """
        This function will calculate the current value of the assets that we have. It will take in the prices of the stocks and then calculate the value of the assets that we have.
        """
        value = self.assets["Money"]
        for symbol, amount in self.assets.items():
            if symbol != "Money":
                value += prices[symbol] * amount
        return value