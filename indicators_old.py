import pandas as pd
import ta

def calculate_indicators(data, window_rsi=14, window_dma=20):
    """
    Calculate RSI and 200 DMA for a given DataFrame.
    Args:
        data (pd.DataFrame): DataFrame containing 'Close' prices.
        window_rsi (int): RSI window length.
        window_dma (int): Short-term DMA window length.
    Returns:
        pd.DataFrame: DataFrame with added RSI and 200 DMA columns.
    """
    # Calculate RSI using the 'ta' library
    data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=window_rsi).rsi().round(0)
    # Calculate 200 DMA
    data['200 DMA'] = data['Close'].rolling(window_dma).mean().round(2)
    # Calculate % Change from 200 DMA
    data['% Change from 200 DMA'] = ((data['Close'] - data['200 DMA']) / data['200 DMA'] * 100).round(2)
    return data

def calculate_daily_indicators(data, window_rsi=14, window_dma=200):
    """
    Calculate RSI and 200 DMA for a given DataFrame.
    Args:
        data (pd.DataFrame): DataFrame containing 'Close' prices.
        window_rsi (int): RSI window length.
        window_dma (int): Long-term DMA window length.
    Returns:
        pd.DataFrame: DataFrame with added RSI and 200 DMA columns.
    """
    # Calculate RSI using the 'ta' library
    data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=window_rsi).rsi().round(0)
    # Calculate 200 DMA
    data['200 DMA'] = data['Close'].rolling(window_dma).mean().round(2)
    # Calculate % Change from 200 DMA
    data['% Change from 200 DMA'] = ((data['Close'] - data['200 DMA']) / data['200 DMA'] * 100).round(2)
    
    # Fill NA values with appropriate methods
    data.fillna(method='bfill', inplace=True)  # Backfill to handle initial NA values
    data.fillna(method='ffill', inplace=True)  # Forward fill to handle any remaining NA values

    return data


