# Import benchmark_utils
from benchmark_utils import load_returns, compute_benchmark, plot_benchmark

# Load data
returns = load_returns("returns.csv")
benchmark_returns, benchmark_cumulative = compute_benchmark(returns)
plot_benchmark(benchmark_cumulative)
