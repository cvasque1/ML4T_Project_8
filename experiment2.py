import StrategyLearner as sl
import marketsimcode as msc
import matplotlib.pyplot as plt

def plot_experiment(values, impacts):
    plt.figure(figsize=(12, 6))

    for value, impact in zip(values, impacts):
        value_normalized = value / value.iloc[0]
        plt.plot(value_normalized.index, value_normalized, label=f"Impact: {impact*100}%")

    plt.title("Strategy Learner Impact")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend(loc="best")
    plt.grid(True, linestyle='--')
    plt.show()

def run_experiment(symbol, in_sd, in_ed, sv):
    impacts = [0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
    values = []

    for impact in impacts:
        learner = sl.StrategyLearner(verbose=False, impact=impact, commission=0.0)
        learner.add_evidence(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
        learner_trades = learner.testPolicy(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
        learner_values = msc.compute_portvals(learner_trades, sd=in_sd, ed=in_ed, start_val=sv)
        values.append(learner_values)

    plot_experiment(values, impacts)

