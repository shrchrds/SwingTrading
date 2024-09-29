import streamlit as st
import pandas as pd
import yfinance as yf

def highlight_trading(row):
    """Highlight rows based on RSI and % Change conditions for Trading Dashboard."""
    if row['Hourly RSI'] < 40 and row['% Change from 20 DMA'] < 0:
        return ['background-color: red'] * len(row)
    elif row['Hourly RSI'] > 75:
        return ['background-color: green'] * len(row)
    return [''] * len(row)

def trading_dashboard(data, etf_list):
    """
    Display trading dashboard with relevant metrics.
    Args:
        data (dict): Dictionary of dataframes for each ETF.
        etf_list (list): List of ETF symbols.
    """
    st.subheader("Based on Hourly RSI and 20 DMA")

    # Prepare a consolidated DataFrame for trading
    trading_data = []
    for etf in etf_list:
        df = data[etf].iloc[-1]  # Select the latest trading day data
        percent_change = ((df['Close'] - df['20 DMA']) / df['20 DMA'] * 100).round(2)
        
        trading_data.append([
            etf.split('.')[0],  # Get ETF name without .NS
            round(df['Close'], 2),
            round(df['RSI'], 2),
            round(df['20 DMA'], 2),
            percent_change
        ])

    # Create a DataFrame and sort by % change from 20 DMA
    trading_df = pd.DataFrame(trading_data, columns=['ETF', 'Close Price', 'Hourly RSI', '20 DMA', '% Change from 20 DMA'])
    trading_df = trading_df.sort_values(by='% Change from 20 DMA')

    # Apply highlighting
    styled_trading_df = trading_df.style.apply(highlight_trading, axis=1)
    
    st.dataframe(styled_trading_df)  # Display the styled DataFrame


def highlight_investing(row):
    """Highlight rows based on RSI, % Change, and TTM P/E conditions for Investing Dashboard."""
    if row['Daily RSI'] < 40 and row['% Change from 200 DMA'] < 0:
        return ['background-color: red'] * len(row)
    elif row['Daily RSI'] > 75:
        return ['background-color: green'] * len(row)

    # Highlight TTM P/E conditions
    if row['TTM P/E'] != "N/A":
        if row['TTM P/E'] < 15:
            return ['background-color: green'] + [''] * (len(row) - 1)
        elif row['TTM P/E'] > 40:
            return ['background-color: red'] + [''] * (len(row) - 1)

    return [''] * len(row)

def investing_dashboard(data, etf_list):
    """
    Display investing dashboard with relevant metrics.
    Args:
        data (dict): Dictionary of dataframes for each ETF.
        etf_list (list): List of ETF symbols.
    """
    st.subheader("Based on Daily RSI and 200 DMA")

    # Prepare a consolidated DataFrame for investing
    investing_data = []
    
    for etf in etf_list:
        df = data[etf].iloc[-1]  # Select the latest trading day data
        percent_change = ((df['Close'] - df['200 DMA']) / df['200 DMA'] * 100).round(2)

        # Fetch TTM P/E ratio
        stock = yf.Ticker(etf)
        pe_ratio = stock.info.get('trailingPE')

        # Format TTM P/E ratio to 2 decimal places
        formatted_pe_ratio = round(pe_ratio, 2) if pe_ratio is not None else "N/A"

        investing_data.append([
            etf.split('.')[0],  # Get ETF name without .NS
            round(df['Close'], 2),
            round(df['RSI'], 2),
            round(df['200 DMA'], 2),
            percent_change,
            formatted_pe_ratio  # Use formatted TTM P/E
        ])

    # Create a DataFrame and sort by % change from 200 DMA
    investing_df = pd.DataFrame(investing_data, columns=['ETF', 'Close Price', 'Daily RSI', '200 DMA', '% Change from 200 DMA', 'TTM P/E'])
    
    investing_df = investing_df.sort_values(by='% Change from 200 DMA')

    # Apply highlighting
    styled_investing_df = investing_df.style.apply(highlight_investing, axis=1)

    st.dataframe(styled_investing_df)  # Display the styled DataFrame
