# Imports
import yfinance as yf
import pandas as pd


# Defining stock simbols thats going to be used
stock_simbols = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'BRK-B', 'META', 'TSLA', 'UNH', 'JPM',
    'V', 'XOM', 'LLY', 'WMT', 'MA', 'PG', 'HD', 'MRK', 'CVX', 'KO',
    'PEP', 'ABBV', 'BAC', 'PFE', 'COST', 'MCD', 'CSCO', 'TMO', 'ACN', 'DIS',
    'ABT', 'DHR', 'INTC', 'VZ', 'CMCSA', 'WFC', 'NKE', 'BMY', 'UPS', 'BA',
    'SPGI', 'AMD', 'GE', 'IBM', 'MMM', 'T', 'CAT', 'HON', 'UNP', 'LOW',
    'ORCL', 'QCOM', 'RTX', 'SBUX', 'MDT', 'GILD', 'DE', 'GS', 'BLK', 'SCHW',
    'AMGN', 'C', 'F', 'MO', 'TGT', 'CI', 'SYK', 'BKNG', 'TJX', 'LMT',
    'PNC', 'CB', 'SO', 'DUK', 'EOG', 'COP', 'AIG', 'D', 'GM', 'MET',
    'VLO', 'AEP', 'SRE', 'OXY', 'HAL', 'ADSK', 'PSX', 'ROP', 'KMB', 'TEL',
    'TRV', 'NEM', 'EBAY', 'JCI', 'ADM', 'DOW', 'YUM', 'CTVA', 'STT', 'BAX'
]

# Setting date range
start_date = "2023-04-10"
end_date = "2024-04-10"

# Loading data
print("Downloading stock data...")
data = yf.download(stock_simbols, start=start_date, end=end_date, auto_adjust=False)['Adj Close'] 

# Dropping stock witch are missing data
ddata = data.dropna(how='any')

# Saving price data
data.to_csv("adjusted_close_prices.csv")

# Calculating daily returns
returns = data.pct_change().dropna()
returns.to_csv("returns.csv")

print(f"Final number of stocks used: {data.shape[1]}")
print(f"Number of return rows: {returns.shape[0]}")
print("Data downloaded and saved as returns.csv")