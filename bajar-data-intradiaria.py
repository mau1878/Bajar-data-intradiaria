import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Set Streamlit app title
st.title('Intraday Stock Data Fetcher')

# Input field for the user to enter a stock ticker
ticker = st.text_input('Enter stock ticker (e.g., AAPL, MSFT, GGAL):')

# Input field for interval selection
interval = st.selectbox('Select the data interval', ['1m', '2m', '5m', '15m', '30m', '1h', '1d'])

# Date picker for selecting the date
selected_date = st.date_input('Select date', value=datetime.today())

# Button to fetch data
if st.button('Fetch Intraday Data'):
    if ticker:
        # Fetch data for the selected date
        start_date = selected_date.strftime('%Y-%m-%d')
        end_date = (selected_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')  # End date is next day to include full day data
        
        try:
            # Fetch intraday data for the selected date and stock ticker
            stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
            
            if not stock_data.empty:
                # Display a sample of the data
                st.write(f"Intraday data for {ticker} on {start_date}:")
                st.dataframe(stock_data.head())

                # Provide the option to download the data as a CSV
                csv = stock_data.to_csv().encode('utf-8')
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f'{ticker}_intraday_data_{start_date}.csv',
                    mime='text/csv',
                )
            else:
                st.error(f"No data available for ticker '{ticker}' on {start_date}.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter a valid stock ticker.")
