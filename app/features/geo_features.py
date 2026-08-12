import numpy as np
import pandas as pd


class GeoFeatures:
    """
    Enterprise Geographic Feature Generator

    Generates:
    - Country
    - City
    - ISP
    - ASN
    - VPN Detection
    - TOR Detection
    - IP Reputation
    - International
    """

    def transform(self, df: pd.DataFrame):

        print("Generating Geo Features...")

        rows = len(df)

        np.random.seed(42)

        ####################################################
        # Country
        ####################################################

        if "Country" not in df.columns:

            df["Country"] = np.random.choice(

                [

                    "US",

                    "IN",

                    "GB",

                    "CA",

                    "AU",

                    "SG",

                    "DE"

                ],

                rows,

                p=[

                    0.42,

                    0.18,

                    0.10,

                    0.10,

                    0.08,

                    0.06,

                    0.06

                ]

            )

        ####################################################
        # City
        ####################################################

        if "City" not in df.columns:

            city_map = {

                "US": "New York",

                "IN": "Hyderabad",

                "GB": "London",

                "CA": "Toronto",

                "AU": "Sydney",

                "SG": "Singapore",

                "DE": "Berlin"

            }

            df["City"] = df["Country"].map(city_map)

        ####################################################
        # ISP
        ####################################################

        if "ISP" not in df.columns:

            df["ISP"] = np.random.choice(

                [

                    "Airtel",

                    "Jio",

                    "Verizon",

                    "AT&T",

                    "Vodafone",

                    "Comcast"

                ],

                rows

            )

        ####################################################
        # ASN
        ####################################################

        if "ASN" not in df.columns:

            df["ASN"] = [

                f"AS{10000+i}"

                for i in range(rows)

            ]

        ####################################################
        # VPN
        ####################################################

        if "VPN_Detection" not in df.columns:

            df["VPN_Detection"] = (

                np.random.rand(rows)

                < 0.08

            )

        ####################################################
        # TOR
        ####################################################

        if "TOR_Detection" not in df.columns:

            df["TOR_Detection"] = (

                np.random.rand(rows)

                < 0.01

            )

        ####################################################
        # International
        ####################################################

        if "International" not in df.columns:

            df["International"] = (

                df["Country"] != "IN"

            )

        ####################################################
        # IP Reputation
        ####################################################

        if "IP_Reputation" not in df.columns:

            amount = df.get(

                "Amount",

                pd.Series(100, index=df.index)

            )

            reputation = (

                amount.rank(pct=True)

                * 40

                +

                np.random.normal(

                    20,

                    10,

                    rows

                )

            )

            df["IP_Reputation"] = (

                reputation

                .clip(0, 100)

                .round(1)

            )

        ####################################################
        # Geo Risk
        ####################################################

        if "Geo_Risk" not in df.columns:

            risk = {

                "US": 15,

                "IN": 20,

                "GB": 18,

                "CA": 16,

                "AU": 15,

                "SG": 12,

                "DE": 14

            }

            df["Geo_Risk"] = (

                df["Country"]

                .map(risk)

                .fillna(20)

            )

        return df