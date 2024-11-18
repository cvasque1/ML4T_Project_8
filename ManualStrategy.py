""""""
"""  		  	   		 	   		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		 	   		  		  		    	 		 		   		 		  

Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 	   		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 	   		  		  		    	 		 		   		 		  

Template code for CS 4646/7646  		  	   		 	   		  		  		    	 		 		   		 		  

Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 	   		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 	   		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 	   		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   		  		  		    	 		 		   		 		  
or edited.  		  	   		 	   		  		  		    	 		 		   		 		  

We do grant permission to share solutions privately with non-students such  		  	   		 	   		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 	   		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 	   		  		  		    	 		 		   		 		  

-----do not edit anything above this line---  		  	   		 	   		  		  		    	 		 		   		 		  

Student Name: Tucker Balch (replace with your name)  		  	   		 	   		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		 	   		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		 	   		  		  		    	 		 		   		 		  
"""

import datetime as dt
import random
import pandas as pd
import matplotlib.pyplot as plt


import marketsimcode as msc
from util import get_data



class ManualStrategy(object):
    """
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output.
    :type verbose: bool
    :param impact: The market impact of each transaction, defaults to 0.0
    :type impact: float
    :param commission: The commission amount charged, defaults to 0.0
    :type commission: float
    """

    # constructor
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """
        Constructor method
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission

        # this method should create a QLearner, and train it for trading

    def add_evidence(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 1, 1),
            sv=100000,
    ):
        """
        Trains your strategy learner over a given time frame.

        :param symbol: The stock symbol to train on
        :type symbol: str
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008
        :type sd: datetime
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009
        :type ed: datetime
        :param sv: The starting value of the portfolio
        :type sv: int
        """
        pass


    def testPolicy(
            self,
            symbol="IBM",
            sd=dt.datetime(2009, 1, 1),
            ed=dt.datetime(2010, 1, 1),
            sv=100000,
    ):
        """
        Tests your learner using data outside of the training data

        :param symbol: The stock symbol that you trained on on
        :type symbol: str
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008
        :type sd: datetime
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009
        :type ed: datetime
        :param sv: The starting value of the portfolio
        :type sv: int
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to
            long so long as net holdings are constrained to -1000, 0, and 1000.
        :rtype: pandas.DataFrame
        """
        # Get symbol prices
        dates = pd.date_range(sd, ed)
        prices = get_data([symbol], dates)
        prices = prices[symbol]

        # Clean data
        prices.fillna(method="ffill", inplace=True)
        prices.fillna(method="bfill", inplace=True)

        # Calculate indicators (SMA, BBp, MACD)
        # sma =
        # bb =
        # macd =


        trades = pd.DataFrame(0, index=prices.index, columns=["Symbol", "Order", "Shares"])
        trades.index.name = "Date"
        position = 0

        # Loops through trading days
        for i in range(len(prices) - 1):
            break


    def benchmark(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 12, 31),
            sv=100000,
    ):
        dates = pd.date_range(sd, ed)
        prices = get_data([symbol], dates)[symbol]

        trades = pd.DataFrame(index=prices.index, columns=["Symbol", "Order", "Shares"])
        trades.index.name = "Date"
        trades.iloc[0] = [symbol, "BUY", 1000]
        trades.dropna(inplace=True)

        values = msc.compute_portvals(trades, sd=sd, ed=ed, start_val=sv)
        values_normalized = values / values.iloc[0]

        return values_normalized


    def plot_benchmark(self, port_values_normalized=None, bm_values_normalized=None):
        """Function to plot the TOS vs. benchmark."""
        plt.figure(figsize=(10, 6))

        # plt.plot(port_values_normalized.index, port_values_normalized, label="Theoretically Optimal Strategy",
        #          color="red")
        plt.plot(bm_values_normalized.index, bm_values_normalized, label="Benchmark", color="purple")

        plt.title("Theoretically Optimal Strategy vs. Benchmark")
        plt.xlabel("Dates")
        plt.ylabel("Normalized Portfolio Value")
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()
        # plt.savefig("./tos_vs_benchmark.png")


    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "cvasquez36"


    def study_group(self):
        """
        :return: A comma separated string of GT_Name of each member of your study group
        :rtype: str
        """
        return "cvasquez36, ewu96, hwang759, kliu353, mma320, mmannerow3, steng31, qliang61"


if __name__ == "__main__":
    manual = ManualStrategy()

    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    symbol = "JPM"

    bm_values_normalized = manual.benchmark(symbol=symbol, sd=sd, ed=ed, sv=sv)

    manual.plot_benchmark(bm_values_normalized=bm_values_normalized)

