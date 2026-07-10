from app.utils.data_loader import load_dataset
from app.features.feature_engineering import FeatureEngineering


def test_feature_engineering():

    df = load_dataset()

    engine = FeatureEngineering(df)

    transformed = engine.run_pipeline()

    assert transformed is not None

    assert len(transformed.columns) > len(df.columns)

    print(transformed.head())

    print(transformed.columns.tolist())


if __name__ == "__main__":

    test_feature_engineering()