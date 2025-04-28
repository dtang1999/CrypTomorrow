import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from db import connect_db

# ---------- 配置 ----------
SEQ_LENGTH = 24  # 输入24小时历史
BATCH_SIZE = 32
EPOCHS = 20
FUTURE_HOURS = 1  # 预测未来1小时收益
CLASSES = [-0.005, 0, 0.005]  # 收益率分区: <-0.5%, [-0.5%,0], [0,0.5%], >0.5%

# ---------- 读取数据 ----------
def load_data(symbol="BTCUSDT"):
    conn = connect_db()
    query = """
        SELECT timestamp, close
        FROM crypto_prices
        WHERE symbol = %s
        ORDER BY timestamp ASC
    """
    df = pd.read_sql(query, conn, params=[symbol])
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# ---------- 处理数据 ----------
def prepare_dataset(df):
    df["return"] = df["close"].pct_change(FUTURE_HOURS).shift(-FUTURE_HOURS)  # 未来1小时收益
    df = df.dropna()

    scaler = MinMaxScaler()
    df["close_scaled"] = scaler.fit_transform(df[["close"]])

    X, y = [], []
    for i in range(len(df) - SEQ_LENGTH):
        x_seq = df["close_scaled"].values[i:i+SEQ_LENGTH]
        future_return = df["return"].values[i+SEQ_LENGTH-1]
        label = np.digitize(future_return, CLASSES)  # 转成分类
        X.append(x_seq)
        y.append(label)

    X = np.array(X)
    y = np.array(y)
    return X, y, scaler

# ---------- 构建模型 ----------
def build_model(input_shape, num_classes):
    model = Sequential([
        LSTM(64, input_shape=input_shape),
        Dense(32, activation="relu"),
        Dense(num_classes, activation="softmax")
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

# ---------- 主程序 ----------
def main():
    df = load_data()
    print(f"数据总量: {len(df)} 条")

    X, y, scaler = prepare_dataset(df)
    print(f"X shape: {X.shape}, y shape: {y.shape}")

    X = X.reshape((X.shape[0], X.shape[1], 1))  # LSTM要求3D: (samples, timesteps, features)

    model = build_model(input_shape=(SEQ_LENGTH, 1), num_classes=len(CLASSES)+1)
    model.summary()

    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2)

    # 保存模型
    model.save("btc_lstm_model.h5")
    print("✅ 训练完成并保存模型。")

if __name__ == "__main__":
    main()
