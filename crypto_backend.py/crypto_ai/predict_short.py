from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from db import connect_db
import pytz

# 设置全局常量
SEQ_LENGTH = 24
CLASSES = [-0.005, 0, 0.005]
LA_TZ = pytz.timezone('America/Los_Angeles')  # 洛杉矶时区

def load_latest_data(symbol="BTCUSDT"):
    conn = connect_db()
    query = """
        SELECT timestamp, close
        FROM crypto_prices
        WHERE symbol = %s
        ORDER BY timestamp DESC
        LIMIT %s
    """
    df = pd.read_sql(query, conn, params=[symbol, SEQ_LENGTH])
    conn.close()
    df = df.sort_values("timestamp")  # 时间升序
    return df

def predict_next_hour():
    model = load_model("btc_lstm_model.h5")

    df = load_latest_data()
    scaler = MinMaxScaler()
    df["close_scaled"] = scaler.fit_transform(df[["close"]])

    X = df["close_scaled"].values.reshape((1, SEQ_LENGTH, 1))  # 单样本输入

    probs = model.predict(X)[0]
    pred_class = np.argmax(probs)

    ranges = ["收益率 < -0.5%", "-0.5% <= 收益率 < 0%", "0% <= 收益率 < 0.5%", "收益率 >= 0.5%"]

    # 时间处理
    latest_timestamp_utc = df["timestamp"].iloc[-1]

    # 假设数据库存的是 UTC 时间，需要转成洛杉矶时间
    latest_timestamp_la = latest_timestamp_utc.tz_convert(LA_TZ)

    predict_start = latest_timestamp_la
    predict_end = latest_timestamp_la + timedelta(hours=1)

    print("=" * 50)
    print(f"🕒 当前数据库最新时间 (UTC): {latest_timestamp_utc.strftime('%Y-%m-%d %H:%M')}")
    print(f"🕒 当前美国洛杉矶时间: {predict_start.strftime('%Y-%m-%d %H:%M')}")
    print(f"🧠 预测时间段: {predict_start.strftime('%Y-%m-%d %H:%M')} ～ {predict_end.strftime('%Y-%m-%d %H:%M')}")
    print(f"📈 预测下一个小时收益区间: {ranges[pred_class]}")
    print(f"📊 各区间概率分布: {probs}")
    print("=" * 50)

if __name__ == "__main__":
    predict_next_hour()
