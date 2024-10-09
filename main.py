import streamlit as st
from datetime import datetime, time
from data_fetcher import get_etf_data
from indicators import calculate_indicators, calculate_daily_indicators
from dashboard import eligible_trading_sidebar, eligible_investing_sidebar, take_trade_sidebar, do_investment_sidebar

# Define the trading hours for the specific window (2:30 PM - 3:20 PM IST)
market_open = time(9, 15)
market_close = time(15, 20)

def is_within_trading_time():
    """Check if the current time is within the trading window."""
    now = datetime.now().time()
    return market_open <= now <= market_close

def main():
    st.sidebar.title("ETF Dashboard Navigation")
    option = st.sidebar.radio("Select Dashboard", ('EligibleTradingETFs', 'EligibleInvestingETFs', 'TakeTrade', 'DoInvestment'))

    etf_codes = [
        'CPSEETF.NS', 'GOLDBEES.NS', 'LOWVOLIETF.NS', 'ALPHAETF.NS', 
        'HDFCMOMENT.NS', 'QUAL30IETF.NS', 'NV20IETF.NS', 
        'MONIFTY500.NS', 'ALPHA.NS', 'ALPL30IETF.NS', 'AUTOIETF.NS', 
        'COMMOIETF.NS', 'DIVOPPBEES.NS', 'BFSI.NS', 'FINIETF.NS', 'FMCGIETF.NS', 
        'CONSUMBEES.NS', 'TNIDETF.NS', 'MAKEINDIA.NS', 'INFRABEES.NS',
        'ITBEES.NS', 'MOM100.NS', 'MNC.NS',
        'JUNIORBEES.NS', 'PHARMABEES.NS', 'PVTBANIETF.NS', 'PSUBNKBEES.NS',
        'HDFCSML250.NS', 'MASPTOP50.NS',
        'ICICIB22.NS', 'MOVALUE.NS',
        'SILVERBEES.NS', 'MONQ50.NS', 'ESG.NS', 'MON100.NS'
    ]

    # Fetch data once and reuse
    etf_data_hourly = get_etf_data(etf_codes, interval='1h', period='3mo')
    etf_data_daily = get_etf_data(etf_codes, interval='1d', period='1y', last_trading_day=True)

    if option == 'EligibleTradingETFs':
        st.title("Eligible Trading ETFs")
        for etf, df in etf_data_hourly.items():
            etf_data_hourly[etf] = calculate_indicators(df, window_rsi=14, window_dma=20)
        eligible_trading_sidebar(etf_data_hourly, etf_codes)

    elif option == 'EligibleInvestingETFs':
        st.title("Eligible Investing ETFs")
        for etf, df in etf_data_daily.items():
            etf_data_daily[etf] = calculate_daily_indicators(df, window_rsi=14, window_dma=200)
        eligible_investing_sidebar(etf_data_daily, etf_codes)

    elif option == 'TakeTrade':
        st.title("Take Trade")
        for etf, df in etf_data_hourly.items():
            etf_data_hourly[etf] = calculate_indicators(df, window_rsi=14, window_dma=200)
        take_trade_sidebar(etf_data_hourly, etf_codes)

    elif option == 'DoInvestment':
        st.title("Do Investment")
        for etf, df in etf_data_daily.items():
            etf_data_daily[etf] = calculate_daily_indicators(df, window_rsi=14, window_dma=200)
        do_investment_sidebar(etf_data_daily, etf_codes)

    if is_within_trading_time():
        st.success("The market is currently open. Data is up-to-date with the latest trading hour.")
    else:
        st.warning("The market is currently closed. Displaying the most recent data from the last trading day.")

if __name__ == "__main__":
    main()