from app.utils.data_loader import DataLoader
from app.features.feature_engineering import FeatureEngineering
from app.ml.preprocessing import DataPreprocessor
from app.xai.shap_explainer import SHAPExplainer


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

    X_test = prep.fit_transform(X_test)

    explainer = SHAPExplainer()
    X_sample = X_test[:500]
    explainer.summary_plot(X_sample)
    explainer.bar_plot(X_sample)
    print("SHAP Completed")


if __name__ == "__main__":
    main()