""""""
"""MC2-P1: Market simulator.  		  	   		 	   		  		  		    	 		 		   		 		  

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

Student Name: Carlos Vasquez (replace with your name)  		  	   		 	   		  		  		    	 		 		   		 		  
GT User ID: cvasquez36 (replace with your User ID)  		  	   		 	   		  		  		    	 		 		   		 		  
GT ID: 904061644 (replace with your GT ID)  		  	   		 	   		  		  		    	 		 		   		 		  
"""

import datetime as dt

import numpy as np

import pandas as pd
from util import get_data, plot_data


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "cvasquez36"  # replace tb34 with your Georgia Tech username.


def study_group():
    """
    :return: A comma separated string of GT_Name of each member of your study group
    :rtype: str
    """
    return "cvasquez36, ewu96, hwang759, kliu353, mma320, mmannerow3, steng31, qliang61"


def get_values(holdings, prices):
    df_trades = holdings * prices

    return df_trades


def get_holdings(trades, start_val):
    df_holdings = trades.cumsum()
    df_holdings['Cash'] += start_val

    return df_holdings


def get_trades(orders, prices, symbols, commission, impact):
    df_trades = pd.DataFrame(0, index=prices.index, columns=symbols + ['Cash'])

    for date, row in orders.iterrows():
        sym, order, shares = row['Symbol'], row['Order'], row['Shares']
        if order == "SELL": shares = -shares
        df_trades.loc[date, sym] += shares
        price = prices.loc[date, sym] * (1 + impact if shares > 0 else 1 - impact)
        df_trades.loc[date, 'Cash'] -= (shares * price + commission)

    return df_trades


def get_prices(symbols, sd, ed):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(symbols, dates)
    prices_all['Cash'] = 1.0

    return prices_all


def compute_portvals(
        orders,
        start_val=100000,
        commission=0.0,
        impact=0.0,
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011,12,31)
):
    """
    Computes the portfolio values.

    :param orders_file: Path of the order file or the file object
    :type orders_file: str or file object
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """
    # Get orders info and extract symbols
    df_orders = orders
    start_date = sd
    end_date = ed

    symbols = df_orders['Symbol'].unique()
    df_prices = get_prices(symbols, start_date, end_date)
    symbols = df_prices.columns[df_prices.columns != 'Cash'].tolist()

    df_trades = get_trades(df_orders, df_prices, symbols, commission, impact)

    df_holdings = get_holdings(df_trades, start_val)

    df_values = get_values(df_holdings, df_prices)

    df_portval = pd.DataFrame(df_values.sum(axis=1), columns=['Portfolio Value'])

    return df_portval


def compute_daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.iloc[0] = 0  # Set the first day to 0
    return daily_returns[1:]  # Ignore the first row


def compute_portfolio_stats(portvals, rfr=0.0, sf=252.0):
    daily_rets = compute_daily_returns(portvals)

    cr = (portvals.iloc[-1] / portvals.iloc[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = np.sqrt(sf) * (adr - rfr) / sddr

    return cr, adr, sddr, sr
