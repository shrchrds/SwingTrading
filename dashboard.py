import streamlit as st
import pandas as pd

def eligible_trading_sidebar(data, etf_list):
    st.sidebar.subheader("Eligible Trading ETFs")
    trading_entries = []
    for etf in etf_list:
        df = data[etf].iloc[-1]
        trading_entries.append({
            'ETF': etf,
            'Close Price': round(df['Close'], 2),
            'RSI': round(df['RSI'], 2),
            '20 DMA': round(df['20 DMA'], 2),
            '% Change from 20 DMA': round(df['% Change from 20 DMA'], 2),
            'Eligible': df['RSI'] < 40 and df['% Change from 20 DMA'] < 0
        })
    
    trading_df = pd.DataFrame(trading_entries)
    st.dataframe(trading_df.style.format(precision=2).applymap(lambda x: 'background-color: yellow' if x else '', subset=['Eligible']))

def eligible_investing_sidebar(data, etf_list):
    st.sidebar.subheader("Eligible Investing ETFs")
    investing_entries = []
    for etf in etf_list:
        df = data[etf].iloc[-1]
        investing_entries.append({
            'ETF': etf,
            'Close Price': round(df['Close'], 2),
            'RSI': round(df['RSI'], 2),
            '200 DMA': round(df['200 DMA'], 2),
            '% Change from 200 DMA': round(((df['Close'] - df['200 DMA']) / df['200 DMA'] * 100), 2),
            'Eligible': df['RSI'] < 40 and ((df['Close'] - df['200 DMA']) / df['200 DMA'] * 100) < 0
        })
    
    investing_df = pd.DataFrame(investing_entries)
    st.dataframe(investing_df.style.format(precision=2).applymap(lambda x: 'background-color: yellow' if x else '', subset=['Eligible']))

def take_trade_sidebar(data, etf_list):
    """Sidebar for taking a trade based on specific criteria."""
    st.sidebar.subheader("Take Trade")
    trading_entries = []
    for etf in etf_list:
        df = data[etf].iloc[-1]  # Select the latest trading hour data
        if df['RSI'] < 40 and df['% Change from 20 DMA'] < 0:
            trading_entries.append({
                'ETF': etf,
                'Close Price': df['Close'],
                'RSI': df['RSI'],
                '20 DMA': df['20 DMA'],
                '% Change from 20 DMA': df['% Change from 20 DMA']
            })
    # Sort by % change from 20 DMA in ascending order
    trading_entries.sort(key=lambda x: x['% Change from 20 DMA'])
    # Select the first ETF to buy
    if trading_entries:
        selected_etf = trading_entries[0]
        st.write(f"Selected ETF for Trading: {selected_etf['ETF']}")
        st.write(f"Reason: Highest drop from 20 DMA with RSI < 40")
        return selected_etf
    else:
        st.write("No ETFs meet the trading criteria.")
        return None

def do_investment_sidebar(data, etf_list):
    """Sidebar for doing an investment based on specific criteria."""
    st.sidebar.subheader("Do Investment")
    investing_entries = []

    for etf in etf_list:
        df = data[etf].iloc[-1]  # Select the latest daily data
        if df['RSI'] < 40 and df['% Change from 200 DMA'] < 0:
            investing_entries.append({
                'ETF': etf,
                'Close Price': df['Close'],
                'RSI': df['RSI'],
                '200 DMA': df['200 DMA'],
                '% Change from 200 DMA': df['% Change from 200 DMA']
            })

    # Sort by % change from 200 DMA in ascending order
    investing_entries.sort(key=lambda x: x['% Change from 200 DMA'])
    # Select the first ETF to buy
    if investing_entries:
        selected_etf = investing_entries[0]
        st.write(f"Selected ETF for Investing: {selected_etf['ETF']}")
        st.write(f"Reason: Highest drop from 200 DMA with RSI < 40")
        return selected_etf
    else:
        st.write("No ETFs meet the investing criteria.")
        return None
