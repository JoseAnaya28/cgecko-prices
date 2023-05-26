import streamlit as st
import requests
import pandas as pd
from datetime import datetime, time
import time
import random

# Define the mapping
symbol_to_coin = {
    'ETH': 'ethereum',
    'SNT': 'status',
    'DAI': 'dai',
    'BTC': 'bitcoin',
    'UNI': 'unicorn-token',
    'RARE': 'superrare',
    'GRT': 'the-graph',
    'OMG': 'omisego',
    'USDT': 'tether',
    'RAD': 'radicle',
    'STETH': 'staked-ether',
    'WETH': 'weth',
    'PAN': 'panvala-pan',
    'SAI': 'sai',
    'BUSD': 'binance-usd',
    'NYM': 'nym',
    'RETH': 'rocket-pool-eth',
    'USDC': 'usd-coin',
    'WSTETH': 'wrapped-steth'
}

# Mapping in reverse
coin_to_symbol = {v: k for k, v in symbol_to_coin.items()}

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

        # Check if 'market_data' and 'current_price' exist in the response and if 'usd', 'chf', and 'eur' exist in 'current_price'
        if 'market_data' in data and 'current_price' in data['market_data']:
            price_usd = data['market_data']['current_price'].get('usd', None)
            price_chf = data['market_data']['current_price'].get('chf', None)
            price_eur = data['market_data']['current_price'].get('eur', None)  # add this line
        else:
            price_usd = price_chf = price_eur = None

        dataframes.append(pd.DataFrame({
            'ID': [id],
            'Symbol': [coin_to_symbol.get(id, '')],
            'Price in USD': [price_usd],
            'Price in CHF': [price_chf],
            'Price in EUR': [price_eur]
        }))

        # Wait 3 seconds between requests
        time.sleep(3)
    
    df = pd.concat(dataframes)
    df.set_index('ID', inplace=True)
    return df

def unix_timestamp(date):
    dt = datetime.combine(date, datetime.min.time())  # convert date to datetime with 00:00:00 time
    return int(dt.timestamp())

def get_crypto_prices_range(start_date, end_date, id, currency):
    url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart/range"
    parameters = {
        'vs_currency': currency,
        'from': unix_timestamp(start_date),
        'to': unix_timestamp(end_date)
    }

    response = requests.get(url, params=parameters)
    data = response.json()

    if 'prices' in data:
        df = pd.DataFrame(data['prices'], columns=['Timestamp', 'Price'])
        df['Symbol'] = coin_to_symbol.get(id, '')  # add symbol
        df['Coin'] = symbol_to_coin.get(coin_to_symbol.get(id, ''), '')  # add coin name
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.date  # convert timestamp to date
        df = df.groupby('Date').last().reset_index()  # keep only the last price of each day
        df.drop(columns={'Timestamp'}, inplace=True)
        df['5 Day MA'] = df['Price'].rolling(window=5).mean()  # 5-day moving average
        df['Best Rate'] = df[['Price', '5 Day MA']].max(axis=1)  # best rate
        df = df.reindex(columns=['Symbol', 'Coin', 'Date', 'Price', '5 Day MA', 'Best Rate'])

    # Wait 3 seconds between requests
    time.sleep(3)

    return df

def main():
    st.title('Crypto Currency Rates')

    ids = ['bitcoin', 'ethereum', 'dai', 'status', 'unicorn-token', 'superrare', 'the-graph', 'omisego', 'tether', 'radicle', 'staked-ether', 'weth', 'panvala-pan', 'sai', 'binance-usd', 'nym', 'rocket-pool-eth', 'usd-coin', 'wrapped-steth']

    with st.sidebar:
        st.header('Single Date Filter')
        date = st.date_input('Select a date', datetime.now())
        fetch_single_date = st.button('Fetch Data for Selected Date')

        st.header('Date Range Filter')
        start_date, end_date = st.date_input('Select a date range', [datetime.now(), datetime.now()])
        id = st.selectbox('Select a cryptocurrency', ids)
        # Currency filter
        currencies = ['USD', 'CHF', 'EUR']
        currency_filter = st.sidebar.selectbox('Select currency to display', currencies, index=0)
        fetch_range_date = st.button('Fetch Data for Date Range')

    # Create a placeholder for the GIF
    gif_placeholder = st.empty()

    # List of GIFs
    gifs = ['1.gif', '2.gif', '3.gif', '4.gif', '5.gif', '6.gif', '7.gif', '8.gif', '9.gif', '10.gif']

    if fetch_single_date:
        with st.spinner('Cooking Data...'):
            # Display a random GIF in the placeholder
            gif_placeholder.image(random.choice(gifs))
            df = get_crypto_prices(date)
        # Clear the GIF placeholder
        gif_placeholder.empty()
        st.success('Data fetched successfully!')
        st.dataframe(df)

    if fetch_range_date:
        with st.spinner('Cooking Data...'):
            # Display a random GIF in the placeholder
            gif_placeholder.image(random.choice(gifs))
            df_range = get_crypto_prices_range(start_date, end_date, id, currency_filter)
        # Clear the GIF placeholder
        gif_placeholder.empty()
        st.success('Data fetched successfully!')
        st.dataframe(df_range)


if __name__ == "__main__":
    main()









