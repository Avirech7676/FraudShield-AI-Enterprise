from app.features.transaction_features import TransactionFeatures
from app.features.device_features import DeviceFeatures
from app.features.geo_features import GeoFeatures
from app.features.merchant_features import MerchantFeatures
from app.features.behavioral_features import BehavioralFeatures
from app.features.rolling_features import RollingFeatures


class FeaturePipeline:
    """
    Enterprise Feature Pipeline

    Runs all feature generators sequentially.
    """

    def __init__(self):

        self.steps = [

            TransactionFeatures(),

            DeviceFeatures(),

            GeoFeatures(),

            MerchantFeatures(),

            BehavioralFeatures(),

            RollingFeatures()

        ]

    ########################################################

    def run(self, dataframe):

        df = dataframe.copy()

        for step in self.steps:

            df = step.transform(df)
            print("\nBefore", step.__class__.__name__)
            print(df.columns.tolist())

            df = step.transform(df)

            print("\nAfter", step.__class__.__name__)
            print(df.columns.tolist())

        return df

    ########################################################

    def __call__(self, dataframe):

        return self.run(dataframe)