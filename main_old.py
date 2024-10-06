import streamlit as st
from datetime import datetime, time
from data_fetcher_old import get_etf_data
from indicators_old import calculate_indicators
from dashboard_old import trading_dashboard, investing_dashboard

# Define ETF list
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

# Sidebar for Navigation
st.sidebar.title("ETF Dashboard Navigation")
option = st.sidebar.radio("Select Dashboard", ('Trading', 'Investing'))

# Define the trading hours for NSE (09:15 AM - 03:30 PM IST)
market_open = time(9, 15)
market_close = time(15, 30)

# Function to check if the market is currently open
def is_market_open():
    now = datetime.now().time()
    return market_open <= now <= market_close

# Fetch and display the dashboard data based on the selected option
if option == 'Trading':
    st.title("ETF Trading Dashboard")
    st.markdown("### Overview of Trading Indicators")
    
    # Fetch hourly data for trading (use interval='1h')
    etf_data = get_etf_data(etf_codes, interval='1h', period='3mo')
    
    # Calculate indicators for the last available hourly data
    for etf, df in etf_data.items():
        etf_data[etf] = calculate_indicators(df, window_rsi=14, window_dma=200)

    # Display the dashboard using the last available data
    trading_dashboard(etf_data, etf_codes)
    
    if is_market_open():
        st.success("The market is currently open. Data is up-to-date with the latest trading hour.")
    else:
        st.warning("The market is currently closed. Displaying the most recent data from the last trading day.")

elif option == 'Investing':
    st.title("ETF Investing Dashboard")
    st.markdown("### Overview of Investing Indicators")
    
    # Fetch daily data for investing (use interval='1d')
    etf_data = get_etf_data(etf_codes, interval='1d', period='1y')
    
    # Calculate indicators for the last available daily data
    for etf, df in etf_data.items():
        etf_data[etf] = calculate_indicators(df, window_rsi=14, window_dma=200)

    # Display the investing dashboard
    investing_dashboard(etf_data, etf_codes)
