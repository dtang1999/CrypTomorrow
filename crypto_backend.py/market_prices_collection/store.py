from db_conn import connect_db
from fetch import get_binance_klines  # 请确保 fetch.py 中使用新的 get_binance_klines(days=30)

def insert_data(df, symbol="BTCUSDT"):
    """Insert K-line data into PostgreSQL"""
    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO crypto_prices (timestamp, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp, symbol) DO NOTHING;
        """, (
            row["timestamp"],
            symbol,
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            row["volume"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ 插入完成，共 {len(df)} 条 {symbol} 数据。")

if __name__ == "__main__":
    # 默认获取过去 30 天的 1 小时数据
    df = get_binance_klines(symbol="BTCUSDT", interval="1h", days=30)
    print("获取数据条数:", len(df))
    print("样例数据:\n", df.head())

    insert_data(df)
