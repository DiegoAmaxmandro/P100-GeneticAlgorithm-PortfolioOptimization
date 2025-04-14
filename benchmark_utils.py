# Imports
import pandas as pd
import matplotlib.pyplot as plt

# Loading data returns from data collection file
def load_returns(path='returns.csv'):
    return pd.read_csv(path, index_col=0, parse_dates=True)

# Function to compute the avage values of the banchmark (equal-weithted version)
def compute_benchmark(returns_df):
    benchmark_returns = returns_df.mean(axis=1)
    benchmark_cumulative = (1 + benchmark_returns).cumprod() #Calculates the cumulative return over time
    return benchmark_returns, benchmark_cumulative

# Plotting cummulativo returns over time
def plot_benchmark(cumulative_returns, title="Simulated S&P 100 Index"):
    plt.figure(figsize=(10, 5))
    cumulative_returns.plot()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
