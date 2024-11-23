import StrategyLearner as sl
import marketsimcode as msc
import matplotlib.pyplot as plt


def plot_portfolio_value(values, impacts):
    plt.figure(figsize=(12, 6))

    for value, impact in zip(values, impacts):
        value_normalized = value / value.iloc[0]
        plt.plot(value_normalized.index, value_normalized, label=f"Impact = {impact}")

    plt.title("Strategy Learner Impact")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend(loc="best")
    plt.grid(True, linestyle='--')
    plt.show()


def plot_cumulative_return(crs, impacts):
    plt.figure(figsize=(12, 6))

    plt.plot(impacts, crs, label="Cumulative Return", marker="o")
    plt.title("Cumulative Return vs Impact")
    plt.xlabel("Impact")
    plt.ylabel("Cumulative Return")
    plt.grid(True, linestyle='--')
    plt.legend(loc="best")
    plt.show()


def plot_num_trades(num_trades, impacts):
    plt.figure(figsize=(12, 6))

    plt.bar(impacts, num_trades, alpha=0.7, width=0.005)
    plt.title("Number of Trades vs Impact")
    plt.xlabel("Impact")
    plt.ylabel("Number of Trades")
    plt.grid(axis="y", linestyle='--')
    plt.show()


def calculate_metrics(values, trades):
    cr = (values.iloc[-1] / values.iloc[0]) - 1
    n_trades = len(trades)
    return cr, n_trades

def run_experiment(symbol, in_sd, in_ed, sv):
    impacts = [0.0, .015, .03, .05, .075, .1, .2, .3]
    values = []
    crs = [] # Cumulative Returns
    num_trades = [] # Number of trades

    for impact in impacts:
        learner = sl.StrategyLearner(verbose=False, impact=impact, commission=0.0)
        learner.add_evidence(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
        learner_trades = learner.testPolicy(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
        learner_values = msc.compute_portvals(learner_trades, sd=in_sd, ed=in_ed, start_val=sv)

        values.append(learner_values)
        cr, n_trades = calculate_metrics(learner_values, learner_trades)
        crs.append(cr)
        num_trades.append(n_trades)

    plot_portfolio_value(values, impacts)
    plot_cumulative_return(crs, impacts)
    plot_num_trades(num_trades, impacts)
