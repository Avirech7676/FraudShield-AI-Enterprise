import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class FeatureEngineering:

    def __init__(self, df):
        self.df = df.copy()
        self.scaler = StandardScaler()

    # -----------------------------
    # Missing Values
    # -----------------------------
    def handle_missing_values(self):

        print("Handling Missing Values...")

        numeric = self.df.select_dtypes(include=np.number).columns

        self.df[numeric] = self.df[numeric].fillna(
            self.df[numeric].median()
        )

        return self.df

    # -----------------------------
    # Remove Duplicates
    # -----------------------------
    def remove_duplicates(self):

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        after = len(self.df)

        print(f"Removed {before-after} duplicate rows.")

        return self.df

    # -----------------------------
    # Time Features
    # -----------------------------
    def create_time_features(self):

        print("Creating Time Features...")

        self.df["Hour"] = (self.df["Time"] // 3600) % 24

        self.df["Minute"] = (self.df["Time"] // 60) % 60

        self.df["Day"] = self.df["Time"] // 86400

        self.df["Night_Transaction"] = (
            self.df["Hour"].isin([0,1,2,3,4,5])
        ).astype(int)

        self.df["Business_Hours"] = (
            self.df["Hour"].between(9,17)
        ).astype(int)

        return self.df

    # -----------------------------
    # Amount Features
    # -----------------------------
    def create_amount_features(self):

        print("Creating Amount Features...")

        self.df["Log_Amount"] = np.log1p(
            self.df["Amount"]
        )

        self.df["High_Value"] = (
            self.df["Amount"] > 1000
        ).astype(int)

        self.df["Very_High_Value"] = (
            self.df["Amount"] > 5000
        ).astype(int)

        self.df["Amount_Squared"] = (
            self.df["Amount"] ** 2
        )

        self.df["Amount_Sqrt"] = np.sqrt(
            self.df["Amount"]
        )

        return self.df

    # -----------------------------
    # Statistical Features
    # -----------------------------
    def create_statistical_features(self):

        print("Creating Statistical Features...")

        if len(self.df) > 1:

            std = self.df["Amount"].std()

            if std == 0:
              std = 1

            self.df["Amount_Zscore"] = (
                self.df["Amount"] -
                self.df["Amount"].mean()
            ) / std

            self.df["Amount_Percentile"] = (
                self.df["Amount"].rank(pct=True)
            )

            self.df["Amount_Bin"] = pd.qcut(
                self.df["Amount"],
                10,
                labels=False,
                duplicates="drop"
            )
        else:
            self.df["Amount_Zscore"] = 0

            self.df["Amount_Percentile"] = 1

            self.df["Amount_Bin"] = 0

        return self.df

    # -----------------------------
    # Interaction Features
    # -----------------------------
    def create_interaction_features(self):

        print("Creating Interaction Features...")

        self.df["V1_V2"] = self.df["V1"] * self.df["V2"]
        self.df["V3_V4"] = self.df["V3"] * self.df["V4"]
        self.df["V5_V6"] = self.df["V5"] * self.df["V6"]
        self.df["V7_V8"] = self.df["V7"] * self.df["V8"]
        self.df["V9_V10"] = self.df["V9"] * self.df["V10"]

        return self.df

    # -----------------------------
    # Scaling
    # -----------------------------
    def scale_features(self):

        print("Scaling Features...")

        columns = self.df.drop(columns=["Class"]).columns

        self.df[columns] = self.scaler.fit_transform(
            self.df[columns]
        )

        return self.df

    # -----------------------------
    # Complete Pipeline
    # -----------------------------
    def run_pipeline(self):

        print("=" * 60)
        print("FEATURE ENGINEERING PIPELINE")
        print("=" * 60)

        self.handle_missing_values()
        self.remove_duplicates()
        self.create_time_features()
        self.create_amount_features()
        self.create_statistical_features()
        self.create_interaction_features()

        print("Feature Engineering Completed.")

        return self.df