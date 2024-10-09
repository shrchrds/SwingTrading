import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=900)  # Cache expires every 3600 seconds (1 hour)
def get_etf_data(etf_list, interval='1h', period='3mo', last_trading_day=False):
    """
    Fetch historical data for a list of ETFs.
    Args:
        etf_list (list): List of ETF ticker symbols.
        interval (str): Data interval ('1d' for daily, '1h' for hourly).
        period (str): Data period (e.g., '3mo' for 3 months).
        last_trading_day (bool): If True, fetch data up to the last trading day.
    Returns:
        dict: Dictionary with ETF symbols as keys and dataframes as values.
    """
    etf_data = {}
    for etf in etf_list:
        df = yf.download(etf, interval=interval, period=period)
        if last_trading_day:
            # Filter to get the last trading day's data
            last_date = df.index.max()
            df = df.loc[df.index == last_date]
        etf_data[etf] = df
    return etf_data
