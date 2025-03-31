import requests
import pandas as pd
from datetime import datetime, timedelta
import time


def get_binance_klines(symbol="BTCUSDT", interval="1h", days=30):
    """Fetch K-line (candlestick) data from Binance API for the past `days`"""
    url = "https://api.binance.us/api/v3/klines"

    end_time = int(time.time() * 1000)  # 当前时间戳（毫秒）
    start_time = int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)

    all_data = []
    limit = 1000  # 每次最多返回 1000 条数据（即 1000 小时）

    while start_time < end_time:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit
        }
        response = requests.get(url, params=params)
        print("API Status:", response.status_code)

        if response.status_code != 200:
            print("API Error:", response.json())
            break

        data = response.json()

        if not data:
            break

        all_data += data
        last_time = data[-1][0]
        start_time = last_time + 1

        time.sleep(0.3)  # 防止 API 限速

    if not all_data:
        print("No data retrieved.")
        return pd.DataFrame()

    df = pd.DataFrame(
        all_data,
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


# 示例运行：获取过去 7 天的 1 小时数据
if __name__ == "__main__":
    df = get_binance_klines(days=7)
    print("共获取数据条数:", len(df))
    print(df.head())
