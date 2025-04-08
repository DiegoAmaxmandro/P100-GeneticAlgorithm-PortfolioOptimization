# Imports
import yfinance as yf
import pandas as pd
import os

# Defining stock simbols
stock_simbols = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'JNJ', 'JPM', 'V', 'PG', 'TSLA',
    'XOM', 'NVDA', 'UNH', 'HD', 'MA', 'BAC', 'PFE', 'KO', 'DIS', 'PEP',
    'CSCO', 'INTC', 'VZ', 'MRK', 'T', 'WMT', 'CVX', 'ABT', 'MCD', 'LLY'
]

# Setting date range
start_date = "2024-04-01"
end_date = "2025-04-01"

# Loading data
print("Loading stock data...")
data = yf.download(stock_simbols, start=start_date, end=end_date)
data = data['Close']

# Dropping stock simbols with missing data
data = data.dropna(axis=1)

# Saving price data (optional)
data.to_csv("adjusted_close_prices.csv")

# Calculating daily returns
returns = data.pct_change().dropna()
returns.to_csv("returns.csv")

print("Data downloaded and saved as returns.csv")