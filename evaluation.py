# Imports
import pandas as pd
import matplotlib.pyplot as plt
from benchmark_utils import load_returns, compute_benchmark

# Evaluation function
def evaluate_portfolio(portfolio, returns_path='returns.csv'):
    returns = load_returns(returns_path)
    benchmark_returns, _ = compute_benchmark(returns)

    selected_returns = returns[portfolio]
    portfolio_returns = selected_returns.mean(axis=1)

    # Ensure dates are sorted
    portfolio_returns = portfolio_returns.sort_index()
    benchmark_returns = benchmark_returns.sort_index()

    # Split into 4 equal quarters
    total_days = len(portfolio_returns)
    quarter_len = total_days // 4

    tracking_errors = []
    cum_returns_portfolio = []
    cum_returns_benchmark = []
    labels = []

    for i in range(4):
        start = i * quarter_len
        end = (i + 1) * quarter_len if i < 3 else total_days

        port_q = portfolio_returns.iloc[start:end]
        bench_q = benchmark_returns.iloc[start:end]

        # Tracking Error (RMSE)
        diff = port_q - bench_q
        te = (diff ** 2).mean() ** 0.5
        tracking_errors.append(te)

        # Cumulative returns
        port_cum = (1 + port_q).cumprod().iloc[-1]
        bench_cum = (1 + bench_q).cumprod().iloc[-1]
        cum_returns_portfolio.append(port_cum)
        cum_returns_benchmark.append(bench_cum)

        labels.append(f"Q{i+1}")

    # Plot tracking error
    plt.figure(figsize=(10, 6))
    plt.plot(labels, tracking_errors, marker='o', label='Tracking Error')
    plt.title("Tracking Error (Portfolio - Benchmark)")
    plt.xlabel("Quarter")
    plt.ylabel("Error")
    plt.legend()
    plt.grid(True)
    plt.savefig("tracking_error_quarters.png")
    plt.show()

    # Plot cumulative returns
    plt.figure(figsize=(10, 6))
    plt.plot(labels, cum_returns_portfolio, marker='o', label='Cumulative Portfolio Return')
    plt.plot(labels, cum_returns_benchmark, marker='s', label='Cumulative Benchmark Return')
    plt.title("Cumulative Returns: Portfolio vs Benchmark")
    plt.xlabel("Quarter")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.savefig("cumulative_returns_quarters.png")
    plt.show()

    return sum(tracking_errors) / len(tracking_errors)