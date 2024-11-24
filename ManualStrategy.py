""""""
from turtledemo.forest import start

from matplotlib.lines import lineStyles

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
import indicators as ind
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
        # Include buffer days for window size to account for non-trading days
        window_size = 20
        buffer_days = window_size * 2
        extended_sd = sd - pd.DateOffset(days=buffer_days)

        # Get symbol prices
        dates = pd.date_range(extended_sd, ed)
        prices_extended = get_data([symbol], dates)[symbol]

        # Calculate indicators (SMA, BBp, MACD)
        sma = ind.calculate_SMA(prices_extended, window_size)
        bbp = ind.calculate_bollinger_bands_percent(prices_extended, sma, window_size)
        momentum = ind.calculate_momentum(prices_extended, window_size)

        # Filter data to original date range
        prices = prices_extended.loc[sd:ed]
        sma = sma.loc[sd:ed]
        bbp = bbp.loc[sd:ed]
        momentum = momentum.loc[sd:ed]

        price_sma_ratio = prices / sma

        # Shift data by one day- use yesterday's value for today's decisions
        price_sma_ratio_shifted = price_sma_ratio.shift(1)
        bbp_shifted = bbp.shift(1)
        momentum_shifted = momentum.shift(1)

        # Indicator thresholds
        sma_buffer = 0.05
        sma_buy = 1.0 - sma_buffer
        sma_sell = 1.0 + sma_buffer

        bbp_buffer = 0.2
        bbp_buy = 0.0 + bbp_buffer
        bbp_sell = 1.0 - bbp_buffer

        momentum_buffer = 0.2
        momentum_buy = 0.0 + momentum_buffer
        momentum_sell = 0.0 - momentum_buffer

        # # Clean data
        # prices.fillna(method="ffill", inplace=True)
        # prices.fillna(method="bfill", inplace=True)

        trades = pd.DataFrame(0, index=prices.index, columns=["Trades"])
        trades.index.name = "Date"
        holdings = 0

        # Loops through trading days
        for i in range(1, len(prices)):
            sma_signal = price_sma_ratio_shifted.iloc[i]
            bbp_signal = bbp_shifted.iloc[i]
            momentum_signal = momentum_shifted.iloc[i]

            sma_b = sma_signal < sma_buy
            sma_s = sma_signal > sma_sell
            bbp_b = bbp_signal < bbp_buy
            bbp_s = bbp_signal > bbp_sell
            momentum_b = momentum_signal > momentum_buy
            momentum_s = momentum_signal < momentum_sell

            buy_signal = (sma_b and bbp_b) or (sma_b and momentum_b) or (bbp_b and momentum_b)
            sell_signal = (sma_s and bbp_s) or (sma_s and momentum_s) or (bbp_s and momentum_s)

            if buy_signal and holdings == 0:
                trades.iloc[i] = 1000
                holdings = 1000
            elif buy_signal and holdings == -1000:
                trades.iloc[i] = 2000
                holdings = 1000
            elif sell_signal and holdings == 0:
                trades.iloc[i] = -1000
                holdings = -1000
            elif sell_signal and holdings == 1000:
                trades.iloc[i] = -2000
                holdings = -1000

        trades.dropna(inplace=True)
        trades = trades[trades["Trades"] != 0]

        return trades


    def benchmark(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 12, 31),
            sv=100000,
    ):
        dates = pd.date_range(sd, ed)
        prices = get_data([symbol], dates)[symbol]

        trades = pd.DataFrame(index=prices.index, columns=["Trades"])
        trades.index.name = "Date"
        trades.iloc[0] = 1000
        trades.dropna(inplace=True)
        values = msc.compute_portvals(
            trades=trades,
            sd=sd,
            ed=ed,
            start_val=sv,
            commission=self.commission,
            impact=self.impact,
            symbol=symbol
        )

        return values


    def plot_benchmark(self, values, bm_values, trades, title):
        """Function to plot the TOS vs. benchmark."""
        plt.figure(figsize=(12, 6))

        values_normalized = values / values.iloc[0]
        bm_values_normalized = bm_values / bm_values.iloc[0]

        plt.plot(values_normalized.index, values_normalized, label="Manual Strategy", color="red")
        plt.plot(bm_values_normalized.index, bm_values_normalized, label="Benchmark", color="purple")

        if trades is not None:
            long_entries = trades[(trades['Trades'] > 0)].index
            short_entries = trades[(trades['Trades'] < 0)].index

            for i, date in enumerate(long_entries):
                plt.axvline(x=date, color='blue', linewidth=0.75, label='LONG Entry' if i == 0 else "")
            for i, date in enumerate(short_entries):
                plt.axvline(x=date, color='black', linewidth=0.75, label='SHORT Entry' if i == 0 else "")


        plt.title(f"Manual Strategy vs. Benchmark for JPM ({title})")
        plt.xlabel("Dates")
        plt.ylabel("Normalized Portfolio Value")
        plt.legend(loc="best")
        plt.grid(True, linestyle='--')
        plt.savefig(f"./manual_strategy_{title}.png")


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

