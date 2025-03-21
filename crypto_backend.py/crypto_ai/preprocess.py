import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from fetch_data import get_crypto_data


def preprocess_data(df, feature="close", sequence_length=50):
    """数据归一化 & 创建时间序列"""
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_scaled = scaler.fit_transform(df[[feature]])

    X, y = [], []
    for i in range(len(df_scaled) - sequence_length):
        X.append(df_scaled[i : i + sequence_length])
        y.append(df_scaled[i + sequence_length])

    return np.array(X), np.array(y), scaler


if __name__ == "__main__":
    df = get_crypto_data()
    X, y, scaler = preprocess_data(df)
    print("数据预处理完成：", X.shape, y.shape)
