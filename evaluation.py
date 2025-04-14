# Imports
import pandas as pd
import matplotlib.pyplot as plt
from benchmark_utils import load_returns, compute_benchmark
import numpy as np

# Evaluation function
def evaluate_portfolio(portfolio, returns_path='returns.csv'):
    returns = load_returns(returns_path)
    benchmark_returns, _ = compute_benchmark(returns)
    
    selected_returns = returns[portfolio]
    portfolio_returns = selected_returns.mean(axis=1)

    # Ensuring dates are sorted
    portfolio_returns = portfolio_returns.sort_index()
    benchmark_returns = benchmark_returns.sort_index()

    # Splitting into 4 equal quarters
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
        
        if port_q.empty or bench_q.empty:
            print(f"Skipping empty quarter {i+1}")
            continue

        # Tracking Error (RMSE)
        diff = port_q - bench_q
        te = (diff ** 2).mean() ** 0.5
        tracking_errors.append(te)

        # Cumulative returns
        port_cum = np.prod(1 + port_q) - 1
        bench_cum = np.prod(1 + bench_q) - 1
        cum_returns_portfolio.append(port_cum)
        cum_returns_benchmark.append(bench_cum)

        labels.append(f"Q{i+1}")
        
        # Correlation
        corr = port_q.corr(bench_q)

        print(f"{i + 1} Quarter:")
        print(f"  Correlation: {corr:.4f}")
        print(f"  Tracking Error: {te:.4f}")
        print(f"  Portfolio Cumulative Return: {port_cum:.4f}")
        print(f"  S&P 100 Cumulative Return: {bench_cum:.4f}\n")

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
    
    # Daily Returns Over Time 
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_returns, label="Portfolio Daily Return")
    plt.plot(benchmark_returns, label="Benchmark Daily Return")
    plt.title("Daily Returns Over Time")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.legend()
    plt.grid(True)
    plt.savefig("GA_daily_returns_over_time.png")
    plt.show()

    # Daily Returns Scatter Plot
    plt.figure(figsize=(8, 6))
    plt.scatter(portfolio_returns, benchmark_returns, alpha=0.7)
    plt.title("Daily Returns: Portfolio vs Benchmark")
    plt.xlabel("Portfolio Daily Return")
    plt.ylabel("Benchmark Daily Return")
    plt.grid(True)
    plt.savefig("GA_daily_return_scatter.png")
    plt.show()

    # Full Period Cumulative Return 
    portfolio_cum = (1 + portfolio_returns).cumprod()
    benchmark_cum = (1 + benchmark_returns).cumprod()

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_cum, label="Portfolio Cumulative Return")
    plt.plot(benchmark_cum, label="Benchmark Cumulative Return")
    plt.title("Cumulative Returns: Portfolio vs. Benchmark")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.savefig("GA_cumulative_returns.png")
    plt.show()

    if len(tracking_errors) == 0:
        print( "No tracking errors calculated — returning 0")
        return 0

    return sum(tracking_errors) / len(tracking_errors)