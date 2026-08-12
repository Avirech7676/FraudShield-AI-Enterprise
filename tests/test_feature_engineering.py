import pandas as pd

from app.features.feature_engineering import FeatureEngineering


def test_features():

    df = pd.DataFrame(

        {

            "Time":[1],

            "Amount":[100],

            **{

                f"V{i}":[0.0]

                for i in range(1,29)

            },

            "Class":[0]

        }

    )

    engine = FeatureEngineering(

        df

    )

    result = engine.run_pipeline()

    assert result is not None

    assert len(result.columns) > len(df.columns)
