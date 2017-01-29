"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    ######### ASSESS PORTFOLIO
    def assess_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), \
                     syms=['GOOG', 'AAPL', 'GLD', 'XOM'], \
                     allocs=[0.1, 0.2, 0.3, 0.4], rfr=0.0, sf=252.0):
        import math
        # Read in adjusted closing prices for given symbols, date range
        dates = pd.date_range(sd, ed)
        prices_all = get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        # Get daily portfolio value
        port_val = prices_SPY  # add code here to compute daily portfolio values
        df = prices.copy()
        df[1:] = (df[1:] / df[0:-1].values)
        for j in range(len(allocs)):
            df.ix[0, j] = allocs[j]

        days = prices.shape[0]
        for i in range(1, days):
            df.ix[i, :] = df.ix[i, :] * df.ix[i - 1, :]
        df['cumm'] = df.sum(axis=1)
        df['daily'] = (df.ix[1:, 'cumm'] / df.ix[0:-1, 'cumm'].values) - 1.
        df['daily_rf'] = df['daily'] - rfr ** (1. / days)
        sr = math.sqrt(sf) * df['daily_rf'].mean() / df['daily_rf'].std()
        cr = df.ix[-1, 'cumm'] - 1
        sddr = df.ix[1:, 'daily'].std()
        adr = df.ix[1:, 'daily'].mean()
        return cr, adr, sddr, sr, df['cumm']*100

    def get_negative_sharpe(allocs,prices ):
        import math
        rfr=0.0
        sf=252.0
        df = prices.copy()
        df[1:] = (df[1:] / df[0:-1].values)
        for j in range(len(allocs)):
            df.ix[0, j] = allocs[j]

        days = prices.shape[0]
        for i in range(1, days):
            df.ix[i, :] = df.ix[i, :] * df.ix[i - 1, :]
        df['cumm'] = df.sum(axis=1)
        df['daily'] = (df.ix[1:, 'cumm'] / df.ix[0:-1, 'cumm'].values) - 1.
        df['daily_rf'] = df['daily'] - rfr ** (1. / days)
        return math.sqrt(sf) * df['daily_rf'].mean() / df['daily_rf'].std() *-1.0

    import scipy.optimize as spo

    def min_sharpe(syms,data,error_func):
        # Init the allocations for the optimal portfolio
        allocs = [0.1 for x in syms]

        #Says one minus the sum of all variables must be zero
        cons = ({'type': 'eq', 'fun': lambda x:  1 - sum(x)})

        #Required to have non negative values
        bnds = tuple((0.0,1.0) for x in allocs)

        result = spo.minimize(error_func,allocs,args=(data,),method='SLSQP',options={'disp':True},constraints=cons,bounds=bnds)
        return result.x

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    allocs = min_sharpe(syms,prices,get_negative_sharpe)
    cr, adr, sddr, sr ,df_cumm= assess_portfolio(sd = sd, ed = ed,syms = syms, allocs = allocs)

    # Get daily portfolio value
    port_val = df_cumm # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        print df_temp.head()
        ax = df_temp.plot(title="Stock prices", fontsize=12)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.show()
        fig = ax.get_figure()
        fig.savefig("comparison_optimal.png")

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
