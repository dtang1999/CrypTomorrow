import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from preprocess import preprocess_data, get_crypto_data

df = get_crypto_data()
X, y, scaler = preprocess_data(df)

model = Sequential(
    [
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1),
    ]
)

model.compile(optimizer="adam", loss="mean_squared_error")

model.fit(X, y, epochs=20, batch_size=32)

model.save("lstm_model.h5")

print("LSTM 训练完成并保存！")
