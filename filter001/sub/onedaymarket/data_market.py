import yfinance as yf
import pandas as pd
from function import *

def fetch_and_process_data(tickers):
    all_data = {}
    for ticker in tickers:
        data = yf.download(ticker, period="max", interval="1d")
        data.reset_index(inplace=True)
        data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y/%m/%d')
        data.sort_values(by='Date', ascending=False, inplace=True)

        if ticker in ["^N225", "^VIX"]:
            data = calculate_macd(data)
        if ticker == "^N225":
            data = calculate_rsi(data)
        all_data[ticker] = data
    return all_data

def calculate_nt_ratio(all_data):
    if "^N225" in all_data and "^TOPX" in all_data:
        n225_data = all_data["^N225"]
        topx_data = all_data["^TOPX"]
        merged_data = pd.merge(n225_data[['Date', 'Close']], topx_data[['Date', 'Close']], on='Date', how='inner')
        merged_data['NT_Ratio'] = merged_data['Close_x'] / merged_data['Close_y']
        all_data["NT_Ratio"] = merged_data[['Date', 'NT_Ratio']]
    return all_data