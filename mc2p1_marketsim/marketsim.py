"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'llee81'


def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000):
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    # GET PRICES OF ALL USED SYMBOLS
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    list_symbols = [i for i in orders_df.Symbol.unique()]
    all_symbols = get_data(list_symbols, pd.date_range(start_date, end_date))

    # ADD ALL SYMBOLS IN orders_df
    for sym in list_symbols:
        orders_df.ix[0, sym] = "0"

    leverage_max = 1.5
    orders_df.ix[0, "cash"] = start_val
    for i in range(orders_df.shape[0]):

        # copy down all symbol holdings
        if i > 0:
            for sym in list_symbols:
                orders_df.ix[i, sym] = orders_df.ix[i - 1, sym]
                orders_df.ix[i, "cash"] = orders_df.ix[i - 1, "cash"]

        # ADD ORDER
        sym = orders_df.ix[i, "Symbol"]
        original_amt = float(orders_df.ix[i, sym])
        add_amt = float(orders_df.ix[i, "Shares"]) if orders_df.ix[i, 'Order'] == 'BUY' else -float(
            orders_df.ix[i, "Shares"])
        orders_df.ix[i, sym] = original_amt + add_amt

        # CASH
        orders_df.ix[i, "stock_price"] = all_symbols.ix[orders_df.index[i], sym]
        orders_df.ix[i, "cash_used"] = -1.0 * orders_df.ix[i, "stock_price"] * add_amt
        orders_df.ix[i, "cash"] = orders_df.ix[i, "cash"] + orders_df.ix[i, "cash_used"]

        # PORTFOLIO VALUE
        stock_value = 0
        leverage_stocks = 0
        for sym in list_symbols:
            stock_value = stock_value + float(orders_df.ix[i, sym]) * float(all_symbols.ix[orders_df.index[i], sym])
            leverage_stocks = leverage_stocks + np.absolute(
                float(orders_df.ix[i, sym]) * float(all_symbols.ix[orders_df.index[i], sym]))

        orders_df.ix[i, "value"] = orders_df.ix[i, "cash"] + stock_value
        orders_df.ix[i, "leverage"] = leverage_stocks / float(orders_df.ix[i, "value"])

        # CHECK OVERLEVERAGE
        if orders_df.ix[i, "leverage"] > 1.5:
            # print 'OVERLEVERAGE: ' , orders_df.index[i]
            for sym in list_symbols:
                orders_df.ix[i, sym] = orders_df.ix[i - 1, sym]
                orders_df.ix[i, "cash"] = orders_df.ix[i - 1, "cash"]

    # print orders_df
    orders_df = orders_df[orders_df.leverage <= 1.5]
    return orders_df.value


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
