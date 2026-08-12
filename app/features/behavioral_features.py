import numpy as np
import pandas as pd


class BehavioralFeatures:
    """
    Enterprise Behavioral Feature Generator
    """

    def transform(self, df: pd.DataFrame):

        print("Generating Behavioral Features...")

        rows = len(df)

        np.random.seed(42)

        ########################################################
        # Transactions Last Hour
        ########################################################

        if "Transactions_Last_Hour" not in df.columns:

            amount = df.get(
                "Amount",
                pd.Series(100, index=df.index)
            )

            activity = (
                amount.rank(pct=True) * 10
                +
                np.random.randint(
                    0,
                    4,
                    rows
                )
            )

            df["Transactions_Last_Hour"] = (
                activity
                .round()
                .clip(0, 20)
                .astype(int)
            )

        ########################################################
        # Transactions Last Day
        ########################################################

        if "Transactions_Last_Day" not in df.columns:

            df["Transactions_Last_Day"] = (

                df["Transactions_Last_Hour"]

                *

                np.random.randint(

                    2,

                    8,

                    rows

                )

            )

        ########################################################
        # Velocity Score
        ########################################################

        if "Velocity_Score" not in df.columns:

            velocity = (

                df["Transactions_Last_Hour"] * 5

                +

                np.random.normal(

                    0,

                    5,

                    rows

                )

            )

            df["Velocity_Score"] = (

                velocity

                .clip(0, 100)

                .round(1)

            )

        ########################################################
        # Login Failure Count
        ########################################################

        if "Login_Failure_Count" not in df.columns:

            df["Login_Failure_Count"] = np.random.poisson(

                1,

                rows

            )

        ########################################################
        # Password Reset
        ########################################################

        if "Password_Reset" not in df.columns:

            df["Password_Reset"] = (

                np.random.rand(rows)

                < 0.05

            )

        ########################################################
        # Device Change
        ########################################################

        if "Device_Change" not in df.columns:

            df["Device_Change"] = (

                np.random.rand(rows)

                < 0.10

            )

        ########################################################
        # Location Jump
        ########################################################

        if "Location_Jump" not in df.columns:

            df["Location_Jump"] = (

                np.random.rand(rows)

                < 0.08

            )

        ########################################################
        # Merchant Diversity
        ########################################################

        if "Merchant_Diversity" not in df.columns:

            df["Merchant_Diversity"] = np.random.randint(

                1,

                10,

                rows

            )

        ########################################################
        # Time Since Last Transaction
        ########################################################

        if "Time_Since_Last_Transaction" not in df.columns:

            df["Time_Since_Last_Transaction"] = np.random.randint(

                1,

                720,

                rows

            )

        ########################################################
        # Behavior Score
        ########################################################

        if "Behavior_Score" not in df.columns:

            score = (

                df["Velocity_Score"] * 0.45

                +

                df["Login_Failure_Count"] * 6

                +

                df["Location_Jump"].astype(int) * 20

                +

                df["Device_Change"].astype(int) * 15

                +

                df["Password_Reset"].astype(int) * 10

            )

            df["Behavior_Score"] = (

                score

                .clip(0, 100)

                .round(1)

            )

        ########################################################
        # Previous Fraud Count
        ########################################################

        if "Previous_Fraud_Count" not in df.columns:

            df["Previous_Fraud_Count"] = np.random.poisson(

                0.2,

                rows

            )

        return df
    