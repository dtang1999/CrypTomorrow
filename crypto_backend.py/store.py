from db_conn import connect_db
from fetch import get_binance_klines

def insert_data(df, symbol="BTCUSDT"):
    """Insert data into PostgreSQL"""
    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO crypto_prices (timestamp, symbol, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (timestamp) DO NOTHING;
        """, (row["timestamp"], symbol, row["open"], row["high"], row["low"], row["close"], row["volume"]))

    conn.commit()
    cursor.close()
    conn.close()

# Fetch data and print the first 5 rows to ensure correctness
df = get_binance_klines()
print("Fetched Data:\n", df.head())  # Debug: Ensure data correctness

# Insert data into the database
insert_data(df)
print("Data successfully stored in the database!")
