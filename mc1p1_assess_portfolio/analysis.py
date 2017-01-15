"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), \
                     syms=['GOOG', 'AAPL', 'GLD', 'XOM'], \
                     allocs=[0.1, 0.2, 0.3, 0.4], \
                     sv=1000000, rfr=0.0, sf=252.0, \
                     gen_plot=False):
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

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        # df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = df['cumm']
        df_temp.plot()

    # Add code here to properly compute end value
    ev = sv * cr

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
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
    test_code()
