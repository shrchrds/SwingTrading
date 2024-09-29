import pandas as pd
import ta

def calculate_indicators(data, window_rsi=14, window_dma=130, window_long_dma=200):
    """
    Calculate RSI, 20 DMA, and 200 DMA for a given DataFrame.
    Args:
        data (pd.DataFrame): DataFrame containing 'Close' prices.
        window_rsi (int): RSI window length.
        window_dma (int): Short-term DMA window length.
        window_long_dma (int): Long-term DMA window length.
    Returns:
        pd.DataFrame: DataFrame with added RSI, 20 DMA, and 200 DMA columns.
    """
    # Calculate RSI using the 'ta' library to ensure values are in the range 0-100
    data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=window_rsi).rsi().round(0)  # Round to integers

    # Calculate 20 DMA and 200 DMA
    data['20 DMA'] = data['Close'].rolling(window_dma).mean().round(2)
    if '200 DMA' not in data.columns:
        data['200 DMA'] = data['Close'].rolling(window_long_dma).mean().round(2)

    return data

def calculate_percentage_change(df, price_col='Close', dma_col='20 DMA'):
    """
    Calculate the percentage change from DMA for each row in the DataFrame.
    Args:
        df (pd.DataFrame): DataFrame containing the price and DMA columns.
        price_col (str): Column name for the price ('Close').
        dma_col (str): Column name for the DMA ('20 DMA' or '200 DMA').
    Returns:
        pd.Series: Series containing the percentage change from DMA.
    """
    return ((df[price_col] - df[dma_col]) / df[dma_col] * 100).round(2)
