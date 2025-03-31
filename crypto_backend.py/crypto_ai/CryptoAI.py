import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os


class CryptoLSTMModel:
    def __init__(self, symbol="BTCUSDT", sequence_length=50):
        self.db_params = {
            "dbname": os.getenv("DB_NAME", "crypto_db"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "password"),
            "host": os.getenv("DB_HOST", "db"),
            "port": os.getenv("DB_PORT", "5432"),
        }
        self.symbol = symbol
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler()
        self.model = None

    def fetch_data(self):
        conn = psycopg2.connect(**self.db_params)
        query = f"""
            SELECT timestamp, close FROM crypto_prices
            WHERE symbol = %s
            ORDER BY timestamp ASC;
        """
        df = pd.read_sql(query, conn, params=(self.symbol,))
        conn.close()
        df.set_index("timestamp", inplace=True)
        df = df.dropna()
        return df

    def preprocess(self, df):
        data_scaled = self.scaler.fit_transform(df)
        X, y = [], []
        for i in range(self.sequence_length, len(data_scaled)):
            X.append(data_scaled[i - self.sequence_length : i])
            y.append(data_scaled[i])
        X, y = np.array(X), np.array(y)

        split = int(len(X) * 0.8)
        return X[:split], y[:split], X[split:], y[split:]

    def build_model(self):
        model = Sequential(
            [
                LSTM(50, return_sequences=True, input_shape=(self.sequence_length, 1)),
                LSTM(50),
                Dense(1),
            ]
        )
        model.compile(optimizer="adam", loss="mean_squared_error")
        self.model = model

    def train(self, X_train, y_train, epochs=10, batch_size=32):
        history = self.model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1,
        )
        return history

    def predict(self, X_test):
        return self.model.predict(X_test)

    def inverse_scale(self, data):
        return self.scaler.inverse_transform(data)

    def plot_predictions(self, actual, predicted, timestamps):
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, actual, label="Actual Price")
        plt.plot(timestamps, predicted, label="Predicted Price", linestyle="--")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title(f"{self.symbol} - LSTM Prediction vs Actual")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("prediction_vs_actual.png")
        plt.close()

    def plot_loss_curve(self, history):
        plt.figure(figsize=(8, 5))
        plt.plot(history.history["loss"], label="Training Loss")
        plt.plot(history.history["val_loss"], label="Validation Loss")
        plt.title(f"{self.symbol} - Training vs Validation Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("training_vs_validation_loss.png")
        plt.close()

    def plot_residuals(self, actual, predicted):
        residuals = actual.flatten() - predicted.flatten()
        plt.figure(figsize=(10, 5))
        plt.scatter(range(len(residuals)), residuals, alpha=0.5)
        plt.axhline(y=0, color="red", linestyle="--")
        plt.title(f"{self.symbol} - Prediction Residuals (Actual - Predicted)")
        plt.xlabel("Time Step")
        plt.ylabel("Residual")
        plt.tight_layout()
        plt.savefig("residuals.png")
        plt.close()

    def plot_residual_histogram(self, actual, predicted):
        residuals = actual.flatten() - predicted.flatten()
        plt.figure(figsize=(8, 5))
        plt.hist(residuals, bins=50, color="gray", edgecolor="black")
        plt.title(f"{self.symbol} - Residual Error Distribution")
        plt.xlabel("Residual (Actual - Predicted)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("residual_histogram.png")
        plt.close()

    def run(self):
        print("Fetching data from database...")
        df = self.fetch_data()
        print("Data shape:", df.shape)

        print("Preprocessing...")
        X_train, y_train, X_test, y_test = self.preprocess(df)

        print("Building and training LSTM model...")
        self.build_model()
        history = self.train(X_train, y_train)

        print("Plotting training vs validation loss...")
        self.plot_loss_curve(history)

        print("Predicting...")
        predictions = self.predict(X_test)

        print("Inversing scale...")
        predicted_prices = self.inverse_scale(predictions)
        actual_prices = self.inverse_scale(y_test.reshape(-1, 1))

        start_idx = self.sequence_length + len(X_train)
        timestamps = df.index[start_idx : start_idx + len(actual_prices)]

        print("Saving prediction vs actual price plot...")
        self.plot_predictions(actual_prices, predicted_prices, timestamps)

        print("Saving residual scatter plot...")
        self.plot_residuals(actual_prices, predicted_prices)

        print("Saving residual histogram plot...")
        self.plot_residual_histogram(actual_prices, predicted_prices)

        rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
        mae = mean_absolute_error(actual_prices, predicted_prices)
        print(f"RMSE: {rmse:.4f}, MAE: {mae:.4f}")


if __name__ == "__main__":
    model = CryptoLSTMModel()
    model.run()
