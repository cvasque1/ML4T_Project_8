import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as msc
import matplotlib.pyplot as plt

def plot_experiment(ms_values, sl_values, bm_values, sample_type, symbol):
    """Function to plot the TOS vs. benchmark."""
    plt.figure(figsize=(12, 6))

    ms_values_normalized = ms_values / ms_values.iloc[0]
    sl_values_normalized = sl_values / sl_values.iloc[0]
    bm_values_normalized = bm_values / bm_values.iloc[0]

    plt.plot(ms_values_normalized.index, ms_values_normalized, label="Manual Strategy", color="red")
    plt.plot(sl_values_normalized.index, sl_values_normalized, label="Strategy Learner", color="blue")
    plt.plot(bm_values_normalized.index, bm_values_normalized, label="Benchmark", color="purple")

    plt.title(f"Manual Strategy vs. Strategy Learner for {symbol} ({sample_type})")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend(loc="best")
    plt.grid(True, linestyle='--')
    plt.savefig(f"experiment1_{sample_type}.png")


def run_experiment(symbol, in_sd, in_ed, out_sd, out_ed, sv):
    # Manual Strategy and Benchmark values (in and out sample)
    manual_strategy = ms.ManualStrategy(impact=0.005, commission=9.95)
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

    # Strategy Learner (in and out sample)
    learner = sl.StrategyLearner(verbose=False, impact=0.005, commission=9.95)
    learner.add_evidence(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
    learner_in_trades = learner.testPolicy(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
    learner_in_values = msc.compute_portvals(
        trades=learner_in_trades,
        sd=in_sd,
        ed=in_ed,
        commission=learner.commission,
        impact=learner.impact, start_val=sv,
        symbol=symbol
    )

    learner_out_trades = learner.testPolicy(symbol=symbol, sd=out_sd, ed=out_ed, sv=sv)
    learner_out_values = msc.compute_portvals(
        trades=learner_out_trades,
        sd=out_sd,
        ed=out_ed,
        commission=learner.commission,
        impact=learner.impact, start_val=sv,
        symbol=symbol
    )

    # Plot in and out sample strategies
    plot_experiment(manual_in_values, learner_in_values, benchmark_in_values, "In-Sample", symbol)
    plot_experiment(manual_out_values, learner_out_values, benchmark_out_values, "Out-Sample", symbol)

