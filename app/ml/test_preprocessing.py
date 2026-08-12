from app.utils.data_loader import DataLoader
from app.features.feature_engineering import FeatureEngineering
from app.ml.preprocessing import DataPreprocessor


if __name__ == "__main__":
    loader = DataLoader(
        "data/raw/creditcard.csv"
    )

    df = loader.load_dataset()

    engine = FeatureEngineering(df)

    df = engine.run_pipeline()

    prep = DataPreprocessor()

    X_train, X_test, y_train, y_test = prep.split_dataset(df)

    prep.identify_columns(X_train)

    prep.build_pipeline()

    X_train = prep.fit_transform(X_train)

    X_test = prep.transform(X_test)

    X_train, y_train = prep.balance_dataset(
        X_train,
        y_train
    )

    prep.save_preprocessor()

    print(X_train.shape)
    print(X_test.shape)
