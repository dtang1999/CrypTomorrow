import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from preprocess import preprocess_data, get_crypto_data
from tensorflow.keras.models import load_model

# Load trained LSTM model
model = load_model("lstm_model.h5")

# Get data
df = get_crypto_data()
X, y, scaler = preprocess_data(df)

# Predict prices
predicted_prices = model.predict(X)

# Inverse transform to get actual prices
predicted_prices = scaler.inverse_transform(predicted_prices.reshape(-1, 1))
actual_prices = scaler.inverse_transform(y.reshape(-1, 1))

# Plot comparison
plt.figure(figsize=(12, 6))
plt.plot(
    df["timestamp"][-len(actual_prices) :],
    actual_prices,
    label="Actual Price",
    color="blue",
)
plt.plot(
    df["timestamp"][-len(predicted_prices) :],
    predicted_prices,
    label="Predicted Price",
    color="red",
    linestyle="dashed",
)
plt.xlabel("Time")
plt.ylabel("Price")
plt.title("LSTM Predicted vs. Actual Prices")
plt.legend()
plt.show()
