import numpy as np
import pandas as pd


class TransactionFeatures:

    def transform(self, df: pd.DataFrame):

        if "Timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df["Transaction_Hour"] = df["Timestamp"].dt.hour
            df["Day_Of_Week"] = df["Timestamp"].dt.dayofweek
            df["Month"] = df["Timestamp"].dt.month

            df["Is_Weekend"] = (
                df["Day_Of_Week"] >= 5
            ).astype(int)

            df["Is_Night"] = (
                (df["Transaction_Hour"] >= 22)
                |
                (df["Transaction_Hour"] <= 6)
            ).astype(int)

        if "Amount" in df.columns:
            df["Log_Amount"] = np.log1p(df["Amount"])
            df["High_Amount"] = (
                df["Amount"] > df["Amount"].quantile(0.95)
            ).astype(int)

            max_amt = max(100000.0, float(df["Amount"].max() if len(df) > 0 else 0) + 1.0)

            df["Amount_Bucket"] = pd.cut(
                df["Amount"],
                bins=[0, 100, 500, 1000, max_amt],
                labels=[
                    "Small",
                    "Medium",
                    "Large",
                    "Very Large"
                ],
                include_lowest=True
            )

        return df
