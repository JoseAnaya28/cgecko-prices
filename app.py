import streamlit as st
import requests
import pandas as pd
from datetime import datetime
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
        time.sleep(3)
    
    df = pd.concat(dataframes)
    df.set_index('ID', inplace=True)
    return df

def main():
    st.title('Crypto Currency Rates')
    date = st.date_input('Select a date', datetime.now())
    df = get_crypto_prices(date)
    st.dataframe(df)

if __name__ == "__main__":
    main()
