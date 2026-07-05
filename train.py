import os

from app.utils.data_loader import DataLoader
from app.features.feature_engineering import FeatureEngineering
from app.ml.preprocessing import DataPreprocessor
from app.ml.trainer import EnterpriseFraudTrainer


def main():

    print("=" * 70)
    print(" FRAUDSHIELD AI ENTERPRISE TRAINING ")
    print("=" * 70)

    ###########################################

    DATASET = "data/raw/creditcard.csv"

    if not os.path.exists(DATASET):

        raise FileNotFoundError(

            f"\nDataset not found:\n{DATASET}"

        )

    ###########################################

    print("\nLoading Dataset...")

    loader = DataLoader(DATASET)

    df = loader.load_dataset()

    ###########################################

    print("\nRunning Feature Engineering...")

    engineer = FeatureEngineering(df)

    df = engineer.run_pipeline()

    ###########################################

    print("\nPreprocessing Dataset...")

    prep = DataPreprocessor(

        target_column="Class"

    )

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

    ###########################################

    print("\nTraining Enterprise Models...")

    trainer = EnterpriseFraudTrainer()

    trainer.run_training_pipeline(

        X_train,

        y_train,

        X_test,

        y_test,

        feature_names=prep.numeric_columns

    )

    ###########################################

    print("\n")

    print("=" * 70)

    print("TRAINING FINISHED SUCCESSFULLY")

    print("=" * 70)


if __name__ == "__main__":

    main()