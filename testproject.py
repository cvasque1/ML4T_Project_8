import datetime as dt
import numpy as np

import ManualStrategy as ms
import experiment1 as e1
import experiment2 as e2
import marketsimcode as msc


def gtid():
    """
    :return: The GT ID of the student
    :rtype: int
    """
    return 904061644 # replace with your GT ID number


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "cvasquez36"


def study_group():
    """
    :return: A comma separated string of GT_Name of each member of your study group
    :rtype: str
    """
    return "cvasquez36, ewu96, hwang759, kliu353, mma320, mmannerow3, steng31, qliang61"


if __name__ == "__main__":
    in_sd = dt.datetime(2008, 1, 1)
    in_ed = dt.datetime(2009, 12, 31)
    out_sd = dt.datetime(2010, 1, 1)
    out_ed = dt.datetime(2011, 12, 31)
    sv = 100000
    symbol = "JPM"

    np.random.seed(gtid())  # do this only once

    #######################
    ### Manual Strategy ###
    #######################

    # In-sample
    manual_strategy = ms.ManualStrategy()
    manual_in_trades = manual_strategy.testPolicy(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
    manual_in_values = msc.compute_portvals(
        trades=manual_in_trades,
        sd=in_sd,
        ed=in_ed,
        start_val=sv,
        commission=manual_strategy.commission,
        impact=manual_strategy.impact,
        symbol=symbol
    )
    benchmark_in_values = manual_strategy.benchmark(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
    manual_strategy.plot_benchmark(manual_in_values, benchmark_in_values, manual_in_trades)

    # Out-sample
    manual_out_trades = manual_strategy.testPolicy(symbol=symbol, sd=out_sd, ed=out_ed, sv=sv)
    manual_out_values = msc.compute_portvals(
        trades=manual_out_trades,
        sd=out_sd,
        ed=out_ed,
        start_val=sv,
        commission=manual_strategy.commission,
        impact=manual_strategy.impact,
        symbol=symbol
    )
    benchmark_out_values = manual_strategy.benchmark(symbol=symbol, sd=out_sd, ed=out_ed, sv=sv)
    manual_strategy.plot_benchmark(manual_out_values, benchmark_out_values, manual_out_trades)


    ####################
    ### Experiment 1 ###
    ####################
    e1.run_experiment(symbol=symbol, in_sd=in_sd, in_ed=in_ed, out_sd=out_sd, out_ed=out_ed, sv=sv)

    ####################
    ### Experiment 2 ###
    ####################
    e2.run_experiment(symbol=symbol, in_sd=in_sd, in_ed=in_ed, sv=sv)