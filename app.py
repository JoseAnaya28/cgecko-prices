import streamlit as st
import requests
import pandas as pd
from datetime import datetime, time
import time


def get_crypto_prices(date):
    ids = ['bitcoin', 'ethereum', 'dai', 'status', 'unicorn-token', 'superrare', 'the-graph', 'omisego', 'tether', 'radicle', 'staked-ether', 'weth', 'panvala-pan', 'sai', 'binance-usd', 'nym', 'rocket-pool-eth', 'usd-coin', 'wrapped-steth']
    dataframes = []

    for id in ids:
        url = f"https://api.coingecko.com/api/v3/coins/{id}/history"
        parameters = {
            'date': date.strftime('%d-%m-%Y'),  # format date as DD-MM-YYYY
            'localization': 'false'
        }
        
        response = requests.get(url, params=parameters)
        data = response.json()

        # Check if 'market_data' and 'current_price' exist in the response and if 'usd' and 'chf' exist in 'current_price'
        if 'market_data' in data and 'current_price' in data['market_data']:
            price_usd = data['market_data']['current_price'].get('usd', None)
            price_chf = data['market_data']['current_price'].get('chf', None)
        else:
            price_usd = price_chf = None

        dataframes.append(pd.DataFrame({'ID': [id], 'Price in USD': [price_usd], 'Price in CHF': [price_chf]}))

        # Wait 3 seconds between requests
        time.sleep(5)
    
    df = pd.concat(dataframes)
    df.set_index('ID', inplace=True)
    return df

def unix_timestamp(date):
    dt = datetime.combine(date, datetime.min.time())  # convert date to datetime with 00:00:00 time
    return int(dt.timestamp())

def get_crypto_prices_range(start_date, end_date):
    ids = ['bitcoin', 'ethereum', 'dai', 'status', 'unicorn-token', 'superrare', 'the-graph', 'omisego', 'tether', 'radicle', 'staked-ether', 'weth', 'panvala-pan', 'sai', 'binance-usd', 'nym', 'rocket-pool-eth', 'usd-coin', 'wrapped-steth']
    dataframes = []
    
    for id in ids:
        url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart/range"
        parameters = {
            'vs_currency': 'usd',
            'from': unix_timestamp(start_date),
            'to': unix_timestamp(end_date)
        }

        response = requests.get(url, params=parameters)
        data = response.json()

        if 'prices' in data:
            prices = [price[1] for price in data['prices']]  # get the price part of each [time, price] pair
            avg_price = sum(prices) / len(prices)
            best_price = max(prices)
        else:
            avg_price = best_price = None

        dataframes.append(pd.DataFrame({'ID': [id], 'Average Price': [avg_price], 'Best Price': [best_price]}))

        # Wait 3 seconds between requests
        time.sleep(5)

    df = pd.concat(dataframes)
    df.set_index('ID', inplace=True)
    return df

def main():
    st.title('Crypto Currency Rates')

    date = st.date_input('Select a date', datetime.now())
    if st.button('Fetch Data for Selected Date'):
        df = get_crypto_prices(date)
        st.dataframe(df)

    start_date, end_date = st.date_input('Select a date range', [datetime.now(), datetime.now()])
    if st.button('Fetch Data for Date Range'):
        st.subheader('Price Range Data')
        df_range = get_crypto_prices_range(start_date, end_date)
        st.dataframe(df_range)

if __name__ == "__main__":
    main()


