# Crypto Currency Rates

This Python script fetches and displays the historical prices of several cryptocurrencies on a specified date using the CoinGecko API. It utilizes the Streamlit library to create a simple web interface.

## Requirements

- Python 3.x
- Streamlit
- Requests
- Pandas

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/JoseAnaya28/cgecko-prices

2. Navigate to the project directory:
    ```bash
    cd your-repo

3. Install the required packages:
    ```bash
    pip install -r requirements.txt

## Usage

1. Run the script:
    ```bash
    streamlit run main.py

2. Open your web browser and access the Streamlit web interface at the provided URL.

3. Select a date from the date picker.

4. The script will fetch the historical prices of the specified cryptocurrencies for the selected date and display them in a table.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The [CoinGecko API](https://coingecko.com/) for providing cryptocurrency data.
- The [Streamlit](https://streamlit.io/) library for creating the web interface.
- The [Pandas](https://pandas.pydata.org/) library for data manipulation.
- The [Requests](https://requests.readthedocs.io/) library for making HTTP requests.
