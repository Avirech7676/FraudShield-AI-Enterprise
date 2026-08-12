import numpy as np
import pandas as pd


class RollingFeatures:
    """
    Enterprise Rolling Feature Generator

    Generates:
    - Previous_Transactions
    - Rolling_Avg_Amount
    - Rolling_Max_Amount
    - Rolling_Min_Amount
    - Rolling_Total_Amount
    - Rolling_Std_Amount
    - Average_Daily_Spend
    - Spending_Trend
    """

    def transform(self, df: pd.DataFrame):

        print("Generating Rolling Features...")

        rows = len(df)

        np.random.seed(42)

        ########################################################
        # Previous Transactions
        ########################################################

        if "Previous_Transactions" not in df.columns:

            df["Previous_Transactions"] = np.random.randint(

                1,

                100,

                rows

            )

        ########################################################
        # Amount
        ########################################################

        amount = df.get(

            "Amount",

            pd.Series(

                np.random.uniform(

                    10,

                    1000,

                    rows

                )

            )

        )

        ########################################################
        # Rolling Average
        ########################################################

        if "Rolling_Avg_Amount" not in df.columns:

            df["Rolling_Avg_Amount"] = (

                amount

                .rolling(

                    5,

                    min_periods=1

                )

                .mean()

                .round(2)

            )

        ########################################################
        # Rolling Max
        ########################################################

        if "Rolling_Max_Amount" not in df.columns:

            df["Rolling_Max_Amount"] = (

                amount

                .rolling(

                    5,

                    min_periods=1

                )

                .max()

            )

        ########################################################
        # Rolling Min
        ########################################################

        if "Rolling_Min_Amount" not in df.columns:

            df["Rolling_Min_Amount"] = (

                amount

                .rolling(

                    5,

                    min_periods=1

                )

                .min()

            )

        ########################################################
        # Rolling Std
        ########################################################

        if "Rolling_Std_Amount" not in df.columns:

            df["Rolling_Std_Amount"] = (

                amount

                .rolling(

                    5,

                    min_periods=1

                )

                .std()

                .fillna(0)

                .round(2)

            )

        ########################################################
        # Rolling Total
        ########################################################

        if "Rolling_Total_Amount" not in df.columns:

            df["Rolling_Total_Amount"] = (

                amount

                .rolling(

                    5,

                    min_periods=1

                )

                .sum()

                .round(2)

            )

        ########################################################
        # Average Daily Spend
        ########################################################

        if "Average_Daily_Spend" not in df.columns:

            df["Average_Daily_Spend"] = (

                df["Rolling_Total_Amount"]

                /

                5

            ).round(2)

        ########################################################
        # Spending Trend
        ########################################################

        if "Spending_Trend" not in df.columns:

            trend = (

                amount

                -

                df["Rolling_Avg_Amount"]

            )

            df["Spending_Trend"] = (

                trend

                .round(2)

            )

        ########################################################
        # High Spending Flag
        ########################################################

        if "High_Spending_Flag" not in df.columns:

            df["High_Spending_Flag"] = (

                amount

                >

                df["Rolling_Avg_Amount"] * 2

            ).astype(int)

        ########################################################
        # Spending Volatility
        ########################################################

        if "Spending_Volatility" not in df.columns:

            df["Spending_Volatility"] = (
                df["Rolling_Std_Amount"]/(df["Rolling_Avg_Amount"]+1)).round(3)
        return df