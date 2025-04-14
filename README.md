# AI-Driven Portfolio Optimizer using Genetic Algorithm

This project implements an AI-based index fund that tracks the **S&P 100** using **fewer than 100 stocks**, based on the requirements of a Continuous Assessment (CA2) for the *AI-Driven Decision Making* module (MSCAI, National College of Ireland).

The solution uses a **Genetic Algorithm (GA)** to select an optimal subset of `q` stocks that best mimics the performance of the S&P 100 over multiple quarters.

---

## Objectives

- Select `q < 100` stocks that replicate the behavior of the S&P 100
- Allocate equal weights to each stock in the portfolio
- Maximize correlation with the S&P 100 benchmark
- Evaluate performance over 1 to 4 quarters using:
  - Correlation
  - Tracking Error (RMSE)
  - Cumulative Return Comparison
- Visualize performance over quarters
- Save results for comparison

---

## Technologies Used

- Python 3.x
- `yfinance` for data collection
- `pandas`, `numpy`, `matplotlib` for data analysis
- `DEAP` for genetic algorithm implementation

---

## Project Structure

```
.
├── data_collection.py            # Downloads S&P 100 data and generates returns.csv
├── genetic_algorithm.py          # GA to select best q-stock portfolio
├── evaluation_by_quarter.py      # Evaluates portfolio vs benchmark across 4 quarters
├── benchmark_utils.py            # Builds equal-weighted benchmark index
├── returns.csv                   # Daily return data
├── ga_results.csv                # CSV log of experiment results
├── tracking_error_quarters.png   # Visual plot saved after evaluation
├── cumulative_returns_quarters.png
```

---

## How to Run

1. Clone the repository

2. Install dependencies:
    ```bash
    pip install yfinance deap pandas matplotlib
    ```

3. Run the scripts in order:
    ```bash
    python data_collection.py
    python genetic_algorithm.py
    ```

---

## Example Output

- `Best Portfolio`: `['AAPL', 'MSFT', 'GOOGL', ...]`
- `Correlation with S&P 100`: `0.925`
- `Tracking Error`: Calculated and visualized per quarter

---

## About Genetic Algorithm

A **Genetic Algorithm** is an optimization method inspired by evolution. It iteratively selects, combines, and mutates portfolios to evolve toward the best-performing solution — in this case, the one that best tracks the S&P 100 index.

---

## Author

- **Name**: Diego Lemos
- **Module**: H9AIDM - AI Driven Decision Making  
- **Institution**: National College of Ireland

---

## License

This project is for educational purposes and not intended for financial advice or real-world trading.
