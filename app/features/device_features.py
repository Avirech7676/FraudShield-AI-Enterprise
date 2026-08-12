import numpy as np
import pandas as pd


class DeviceFeatures:
    """
    Generates enterprise device intelligence features.
    """

    def transform(self, df: pd.DataFrame):

        print("Generating Device Features...")

        rows = len(df)

        np.random.seed(42)

        ########################################################
        # Browser
        ########################################################

        if "Browser" not in df.columns:

            df["Browser"] = np.random.choice(

                [

                    "Chrome",

                    "Safari",

                    "Firefox",

                    "Edge",

                    "Opera"

                ],

                rows,

                p=[

                    0.52,

                    0.20,

                    0.12,

                    0.11,

                    0.05

                ]

            )

        ########################################################
        # Operating System
        ########################################################

        if "Operating_System" not in df.columns:

            df["Operating_System"] = np.random.choice(

                [

                    "Windows",

                    "Android",

                    "iOS",

                    "MacOS",

                    "Linux"

                ],

                rows,

                p=[

                    0.45,

                    0.25,

                    0.15,

                    0.10,

                    0.05

                ]

            )

        ########################################################
        # Device Trust Score
        ########################################################

        if "Device_Trust_Score" not in df.columns:

            amount = df.get(
                "Amount",
                pd.Series(100, index=df.index)
            )

            trust = (

                100

                - amount.rank(pct=True) * 25

                - np.random.uniform(

                    0,

                    10,

                    rows

                )

            )

            df["Device_Trust_Score"] = (

                trust

                .clip(0, 100)

                .round(1)

            )

        ########################################################
        # Emulator
        ########################################################

        if "Emulator_Detection" not in df.columns:

            df["Emulator_Detection"] = (

                np.random.rand(rows)

                < 0.02

            )

        ########################################################
        # Rooted
        ########################################################

        if "Rooted_Device" not in df.columns:

            df["Rooted_Device"] = (

                np.random.rand(rows)

                < 0.03

            )

        ########################################################
        # Jailbreak
        ########################################################

        if "Jailbreak_Detection" not in df.columns:

            df["Jailbreak_Detection"] = (

                np.random.rand(rows)

                < 0.02

            )

        ########################################################
        # Device Fingerprint
        ########################################################

        if "Device_Fingerprint" not in df.columns:

            df["Device_Fingerprint"] = [

                f"DEV-{100000+i}"

                for i in range(rows)

            ]

        return df