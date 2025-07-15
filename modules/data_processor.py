# Data loading/cleaning
# modules/data_processor.py

import pandas as pd
import numpy as np

class DataProcessor:
    @staticmethod
    def load_data(path):
        return pd.read_csv(path)

    @staticmethod
    def clean_data(df):
        df = df.copy()
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df = df.dropna(subset=["TotalCharges"])
        df = df.drop_duplicates()

        if "Churn" in df.columns:
            df["Churn"] = df["Churn"].apply(lambda x: 1 if str(x).strip().lower() == "yes" else 0)

        return df

    @staticmethod
    def transform(df):
        df = df.copy()

        if "customerID" in df.columns:
            df = df.drop(columns=["customerID"])

        if "Churn" not in df.columns:
            raise ValueError("❌ 'Churn' column not found")

        X = df.drop(columns=["Churn"])
        y = df["Churn"]

        X = pd.get_dummies(X, drop_first=True)
        X = X.astype(np.float64)

        return X, y
