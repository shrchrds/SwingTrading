import yfinance as yf

def get_etf_data(etf_codes, interval='1d', period='1y', last_trading_day=False):
    """
    Fetch ETF data using yfinance.
    Args:
        etf_codes (list): List of ETF symbols.
        interval (str): Data interval.
        period (str): Data period.
        last_trading_day (bool): Whether to fetch data up to the last trading day.
    Returns:
        dict: Dictionary of DataFrames for each ETF.
    """
    etf_data = {}
    for etf in etf_codes:
        df = yf.download(etf, interval=interval, period=period)
        if last_trading_day:
            df = df[df.index <= df.index.max()]  # Ensure data is up to the last trading day
        etf_data[etf] = df
    return etf_data
