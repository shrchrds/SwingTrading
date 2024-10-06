import yfinance as yf
import pandas as pd

def get_etf_data(etf_list, interval='1d', period='1y'):
    """
    Fetch historical data for a list of ETFs.
    Args:
        etf_list (list): List of ETF ticker symbols.
        interval (str): Data interval ('1d' for daily, '1h' for hourly).
        period (str): Data period (e.g., '1y' for 1 year).
    Returns:
        dict: Dictionary with ETF symbols as keys and dataframes as values.
    """
    etf_data = {}
    for etf in etf_list:
        etf_data[etf] = yf.download(etf, interval=interval, period=period)
    return etf_data
