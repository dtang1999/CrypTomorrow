import requests
import pandas as pd


def get_binance_klines(symbol="BTCUSDT", interval="1h", limit=100):
    """Fetch K-line (candlestick) data from Binance API"""
    url = "https://api.binance.us/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)

    # Print API response status code
    print("API Response Status Code:", response.status_code)

    # If the status code is not 200, print the error message
    if response.status_code != 200:
        print("API Error:", response.json())
        return pd.DataFrame()

    data = response.json()

    # Ensure the response is a list
    if not isinstance(data, list):
        print("Unexpected API Response:", data)
        return pd.DataFrame()

    # Print the first two rows of data
    print("API Response Data (first 2 rows):", data[:2])

    df = pd.DataFrame(
        data,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df[["timestamp"] + numeric_cols]


# Run test
df = get_binance_klines()
print("Final retrieved data:\n", df.head())
