import pandas as pd
from datetime import datetime, timedelta
import os

def update_journal(selected_etf, journal_type):
    """
    Update the trading or investment journal with the selected ETF.
    
    Args:
        selected_etf (dict): Dictionary containing selected ETF details.
        journal_type (str): Type of journal to update ('trade' or 'investment').
    """
    # Define the file path
    file_path = f"{journal_type}_journal.xlsx"
    
    # Create a DataFrame for the new entry
    new_entry = pd.DataFrame([{
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Time': datetime.now().strftime('%H:%M:%S'),
        'ETF': selected_etf['ETF'],
        'Close Price': round(selected_etf['Close Price'], 2),
        'RSI': selected_etf['RSI'],
        'DMA': selected_etf['20 DMA'] if journal_type == 'trade' else selected_etf['200 DMA'],
        '% Change from DMA': selected_etf['% Change from 20 DMA'] if journal_type == 'trade' else selected_etf['% Change from 200 DMA'],
        'Quantity': (20000 // selected_etf['Close Price'] + 1) if journal_type == 'trade' else (50000 // selected_etf['Close Price'] + 1),
        'CapitalInvested': round((20000 // selected_etf['Close Price'] + 1) * selected_etf['Close Price'] if journal_type == 'trade' else (50000 // selected_etf['Close Price'] + 1) * selected_etf['Close Price']),
        'Sell Date': None,
        'Sell Price': None,
        'Profit/Loss': None
    }])
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing journal
        existing_journal = pd.read_excel(file_path)
        # Append the new entry
        updated_journal = pd.concat([existing_journal, new_entry], ignore_index=True)
    else:
        # If the file doesn't exist, the new entry is the updated journal
        updated_journal = new_entry
    
    # Save the updated journal back to the Excel file
    updated_journal.to_excel(file_path, index=False)

def check_and_update_sell(df, etf, journal_type):
    """
    Check if the sell conditions are met and update the journal.
    
    Args:
        df (pd.DataFrame): DataFrame containing ETF data.
        etf (str): ETF ticker symbol.
        journal_type (str): Type of journal to update ('trade' or 'investment').
    """
    file_path = f"{journal_type}_journal.xlsx"
    
    if not os.path.exists(file_path):
        return
    
    journal = pd.read_excel(file_path)
    current_price = df['Close'].iloc[-1]
    
    for index, row in journal.iterrows():
        if pd.isna(row['Sell Date']) and row['ETF'] == etf:
            buy_price = row['Close Price']
            if journal_type == 'trade':
                # Check for 6% profit
                if current_price >= buy_price * 1.06:
                    journal.at[index, 'Sell Date'] = datetime.now().strftime('%Y-%m-%d')
                    journal.at[index, 'Sell Price'] = current_price
                    journal.at[index, 'Profit/Loss'] = (current_price - buy_price) * row['Quantity']
            elif journal_type == 'investment':
                # Check for 20% profit and 1 year holding
                buy_date = datetime.strptime(row['Date'], '%Y-%m-%d')
                if current_price >= buy_price * 1.20 and datetime.now() >= buy_date + timedelta(days=365):
                    journal.at[index, 'Sell Date'] = datetime.now().strftime('%Y-%m-%d')
                    journal.at[index, 'Sell Price'] = current_price
                    journal.at[index, 'Profit/Loss'] = (current_price - buy_price) * row['Quantity']
    
    # Save the updated journal back to the Excel file
    journal.to_excel(file_path, index=False)
