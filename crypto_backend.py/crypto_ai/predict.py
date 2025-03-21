import numpy as np
import tensorflow as tf
from preprocess import preprocess_data, get_crypto_data
from tensorflow.keras.models import load_model
import pandas as pd


# 加载训练好的 LSTM 模型
model = load_model("lstm_model.h5")

# 获取最新数据
df = get_crypto_data()
X, _, scaler = preprocess_data(df)

# 预测下一个时间步的价格
predicted_price = model.predict(X[-1].reshape(1, X.shape[1], 1))

# 反归一化
predicted_price = scaler.inverse_transform(predicted_price.reshape(-1, 1))

# 获取最后一个时间点，并推算预测时间
last_timestamp = df["timestamp"].iloc[-1]  # 取最后一个时间
predicted_timestamp = last_timestamp + pd.Timedelta(hours=1)  # 预测 1 小时后的价格

print(f"预测时间: {predicted_timestamp}")
print(f"预测的未来价格: {predicted_price[0][0]:.2f}")
