from app.utils.data_loader import DataLoader
from app.features.feature_engineering import FeatureEngineering
from app.ml.preprocessing import DataPreprocessor
from app.anomaly.detector import EnterpriseAnomalyDetector


def main():

    loader = DataLoader(

        "data/raw/creditcard.csv"

    )

    df = loader.load_dataset()

    engineer = FeatureEngineering(df)

    df = engineer.run_pipeline()

    prep = DataPreprocessor()

    X_train, X_test, y_train, y_test = prep.split_dataset(df)

    prep.identify_columns(X_train)

    prep.build_pipeline()

    X_train = prep.fit_transform(X_train)

    X_test = prep.transform(X_test)

    detector = EnterpriseAnomalyDetector()

    detector.train(X_train)

    detector.load()

    prediction, score = detector.predict(

        X_test[:5]

    )

    print()

    print("Prediction")

    print(prediction)

    print()

    print("Anomaly Score")

    print(score)



if __name__ == "__main__":

    main()