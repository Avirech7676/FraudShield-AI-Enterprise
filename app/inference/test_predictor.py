from app.utils.data_loader import DataLoader
from app.features.feature_engineering import FeatureEngineering
from app.inference.predictor import EnterpriseFraudPredictor


def main():

    print("=" * 60)
    print("TESTING ENTERPRISE PREDICTOR")
    print("=" * 60)

    # Load dataset
    loader = DataLoader("data/raw/creditcard.csv")
    df = loader.load_dataset()

    # Run feature engineering
    engineer = FeatureEngineering(df)
    df = engineer.run_pipeline()

    # Take one sample (remove target column)
    sample = df.drop(columns=["Class"]).head(1)

    # Load predictor
    predictor = EnterpriseFraudPredictor()

    # Predict
    result = predictor.predict_single(sample)

    print("\nPrediction Result")
    print("=" * 60)
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    main()
