import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler

from imblearn.over_sampling import SMOTE


class DataPreprocessor:

    def __init__(
        self,
        target_column="Class",
        test_size=0.20,
        random_state=42
    ):

        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state

        self.numeric_columns = None

        self.preprocessor = None

    ##########################################################

    def split_dataset(self, df):

        X = df.drop(columns=[self.target_column])

        y = df[self.target_column]

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=self.test_size,

            stratify=y,

            random_state=self.random_state

        )

        return X_train, X_test, y_train, y_test

    ##########################################################

    def identify_columns(self, X):

        self.numeric_columns = X.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        return self.numeric_columns

    ##########################################################

    def build_pipeline(self):

        numeric_pipeline = Pipeline(

            steps=[

                ("scaler", RobustScaler())

            ]

        )

        self.preprocessor = ColumnTransformer(

            transformers=[

                (

                    "numeric",

                    numeric_pipeline,

                    self.numeric_columns

                )

            ]

        )

        return self.preprocessor

    ##########################################################

    def fit_transform(self, X_train):

        X_train = self.preprocessor.fit_transform(
            X_train
        )

        return X_train

    ##########################################################

    def transform(self, X_test):

        return self.preprocessor.transform(
            X_test
        )

    ##########################################################

    def balance_dataset(
        self,
        X_train,
        y_train
    ):

        print("\nApplying SMOTE...")

        smote = SMOTE(
            random_state=self.random_state
        )

        X_balanced, y_balanced = smote.fit_resample(

            X_train,
            y_train

        )

        print("Dataset Balanced Successfully")

        print(y_balanced.value_counts())

        return X_balanced, y_balanced

    ##########################################################

    def save_preprocessor(
        self,
        filepath="models/preprocessor.joblib"
    ):

        os.makedirs("models", exist_ok=True)

        joblib.dump(
            self.preprocessor,
            filepath
        )

        print(f"Saved preprocessor -> {filepath}")

    ##########################################################

    def load_preprocessor(
        self,
        filepath="models/preprocessor.joblib"
    ):

        self.preprocessor = joblib.load(filepath)

        return self.preprocessor