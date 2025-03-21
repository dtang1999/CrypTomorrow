import pandas as pd
from db import connect_db


def get_crypto_data(symbol="BTCUSDT", limit=1000):
    """从数据库获取历史 K 线数据"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT timestamp, open, high, low, close, volume FROM crypto_prices
    WHERE symbol = %s ORDER BY timestamp ASC LIMIT %s;
    """,
        (symbol, limit),
    )

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(
        data, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


if __name__ == "__main__":
    df = get_crypto_data()
    print(df.head())
