import numpy as np
import pandas as pd


class MerchantFeatures:
    """
    Enterprise Merchant Feature Generator
    """

    def transform(self, df: pd.DataFrame):

        print("Generating Merchant Features...")

        rows = len(df)

        np.random.seed(42)

        ########################################################
        # Merchant
        ########################################################

        if "Merchant" not in df.columns:

            merchants = [

                "Amazon",
                "Walmart",
                "Target",
                "Apple",
                "Netflix",
                "Steam",
                "Uber",
                "Airbnb",
                "BestBuy",
                "eBay"

            ]

            df["Merchant"] = np.random.choice(

                merchants,

                rows,

                p=[

                    0.20,
                    0.18,
                    0.12,
                    0.08,
                    0.08,
                    0.06,
                    0.10,
                    0.05,
                    0.08,
                    0.05

                ]

            )

        ########################################################
        # Merchant Category
        ########################################################

        if "Merchant_Category" not in df.columns:

            category_map = {

                "Amazon": "Retail",

                "Walmart": "Retail",

                "Target": "Retail",

                "Apple": "Electronics",

                "BestBuy": "Electronics",

                "Netflix": "Entertainment",

                "Steam": "Entertainment",

                "Uber": "Travel",

                "Airbnb": "Travel",

                "eBay": "Marketplace"

            }

            df["Merchant_Category"] = (

                df["Merchant"]

                .map(category_map)

                .fillna("Retail")

            )

        ########################################################
        # Merchant Risk
        ########################################################

        if "Merchant_Risk" not in df.columns:

            risk_map = {

                "Retail": 20,

                "Electronics": 35,

                "Entertainment": 45,

                "Travel": 55,

                "Marketplace": 65

            }

            base_risk = (

                df["Merchant_Category"]

                .map(risk_map)

                .astype(float)

            )

            noise = np.random.normal(

                0,

                5,

                rows

            )

            df["Merchant_Risk"] = (

                base_risk

                +

                noise

            ).clip(

                0,

                100

            ).round(1)

        ########################################################
        # Merchant Chargeback Rate
        ########################################################

        if "Merchant_Chargeback_Rate" not in df.columns:

            df["Merchant_Chargeback_Rate"] = (

                df["Merchant_Risk"]

                / 100

                *

                np.random.uniform(

                    0.5,

                    4.5,

                    rows

                )

            ).round(2)

        ########################################################
        # Merchant Country
        ########################################################

        if "Merchant_Country" not in df.columns:

            if "Country" in df.columns:

                df["Merchant_Country"] = df["Country"]

            else:

                df["Merchant_Country"] = np.random.choice(

                    [

                        "US",

                        "IN",

                        "GB",

                        "CA",

                        "AU"

                    ],

                    rows

                )

        ########################################################
        # High Risk Merchant
        ########################################################

        if "High_Risk_Merchant" not in df.columns:

            df["High_Risk_Merchant"] = (

                df["Merchant_Risk"] >= 60

            ).astype(int)

        ########################################################
        # Merchant Age (Months)
        ########################################################

        if "Merchant_Age_Months" not in df.columns:

            df["Merchant_Age_Months"] = np.random.randint(

                6,

                120,

                rows

            )

        return df