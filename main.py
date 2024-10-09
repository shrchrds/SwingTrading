import streamlit as st
from datetime import datetime, time, timedelta
from data_fetcher import get_etf_data
from indicators import calculate_indicators, calculate_daily_indicators
from dashboard import eligible_trading_sidebar, eligible_investing_sidebar, take_trade_sidebar, do_investment_sidebar
from journal import update_journal, check_and_update_sell
import pytz

# Define the trading hours for the specific window (2:30 PM - 3:15 PM IST)
market_open = time(14, 30)
market_close = time(23, 15)

# Define the IST timezone
ist_timezone = pytz.timezone('Asia/Kolkata')

def is_within_trading_time():
    """Check if the current time is within the trading window."""
    current_time_ist = datetime.now(ist_timezone).time()
    return market_open <= current_time_ist <= market_close

def main():
    st.sidebar.title("ETF Dashboard Navigation")
    option = st.sidebar.radio("Select Dashboard", ('EligibleTradingETFs', 'EligibleInvestingETFs', 'TakeTrade', 'DoInvestment', 'CheckSellConditions'))

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

    if option == 'EligibleTradingETFs':
        st.title("Eligible Trading ETFs")
        etf_data = get_etf_data(etf_codes, interval='1h', period='3mo')
        for etf, df in etf_data.items():
            etf_data[etf] = calculate_indicators(df, window_rsi=14, window_dma=20)
        eligible_trading_sidebar(etf_data, etf_codes)

    elif option == 'EligibleInvestingETFs':
        st.title("Eligible Investing ETFs")
        etf_data = get_etf_data(etf_codes, interval='1d', period='1y', last_trading_day=True)
        for etf, df in etf_data.items():
            etf_data[etf] = calculate_daily_indicators(df, window_rsi=14, window_dma=200)
        eligible_investing_sidebar(etf_data, etf_codes)

    elif option == 'TakeTrade':
        st.title("Take Trade")
        etf_data = get_etf_data(etf_codes, interval='1h', period='3mo')
        for etf, df in etf_data.items():
            etf_data[etf] = calculate_indicators(df, window_rsi=14, window_dma=20)
        selected_etf = take_trade_sidebar(etf_data, etf_codes)
        if selected_etf:
            update_journal(selected_etf, 'trade')

    elif option == 'DoInvestment':
        st.title("Do Investment")
        etf_data = get_etf_data(etf_codes, interval='1d', period='1y')
        for etf, df in etf_data.items():
            etf_data[etf] = calculate_daily_indicators(df, window_rsi=14, window_dma=200)
        selected_etf = do_investment_sidebar(etf_data, etf_codes)
        if selected_etf:
            update_journal(selected_etf, 'investment')

    elif option == 'CheckSellConditions':
        st.title("Check Sell Conditions")
        etf_data = get_etf_data(etf_codes, interval='1d', period='1y')
        for etf, df in etf_data.items():
            check_and_update_sell(df, etf, 'trade')
            check_and_update_sell(df, etf, 'investment')

    if is_within_trading_time():
        st.success("The market is currently open. Data is up-to-date with the latest trading hour.")
    else:
        st.warning("The market is currently closed. Displaying the most recent data from the last trading day.")

if __name__ == "__main__":
    main()
