import pandas as pd
from datetime import datetime, time

# Define the trading hours (e.g., 09:15 AM to 03:30 PM)
market_open = time(9, 15)
market_close = time(15, 30)

def is_within_trading_time():
    """Check if the current time is within the trading hours."""
    now = datetime.now().time()
    return market_open <= now <= market_close


def identify_trading_entries(etf_data, total_capital=1000000, utilized_capital=0, investment_per_trade=20000):
    """
    Identify trading entries based on the given strategy within the specified trading time.
    
    Args:
        etf_data (dict): Dictionary with ETF symbols as keys and dataframes as values.
        total_capital (float): Total capital available for investment.
        utilized_capital (float): Capital already utilized in previous trades.
        investment_per_trade (float): Fixed amount to invest per trade.
    
    Returns:
        pd.DataFrame: DataFrame containing trading entries.
    """
    if not is_within_trading_time():
        print("Not within trading time.")
        return pd.DataFrame(columns=['ETF', 'Close Price', 'Quantity', 'Investment', 'Highlight'])

    available_capital = total_capital - utilized_capital
    trading_entries = []

    for etf, df in etf_data.items():
        # Get the latest data
        latest_data = df.iloc[-1]
        
        # Check the buy condition
        if latest_data['Hourly RSI'] < 40 and latest_data['% Change from 20 DMA'] < 0:
            trading_entries.append({
                'ETF': etf,
                'Close Price': latest_data['Close'],
                '% Change from 20 DMA': latest_data['% Change from 20 DMA']
            })

    # Sort by % change from 20 DMA in ascending order
    trading_entries.sort(key=lambda x: x['% Change from 20 DMA'])

    # Select the first ETF to buy
    if trading_entries and available_capital >= investment_per_trade:
        selected_etf = trading_entries[0]
        close_price = selected_etf['Close Price']
        quantity = investment_per_trade // close_price

        # Create a DataFrame for the selected ETF
        trading_df = pd.DataFrame([{
            'ETF': selected_etf['ETF'],
            'Close Price': close_price,
            'Quantity': quantity,
            'Investment': quantity * close_price
        }])

        # Highlight in green if the current price is more than 6% above the purchase price
        trading_df['Highlight'] = trading_df.apply(
            lambda row: 'background-color: green' if row['Close Price'] > 1.06 * close_price else '',
            axis=1
        )

        return trading_df

    return pd.DataFrame(columns=['ETF', 'Close Price', 'Quantity', 'Investment', 'Highlight'])



