import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer

class DataPreprocessor:
    """
    Data Preprocessor
    Splits, preprocesses (RobustScaler + OneHotEncoder), and balances (SMOTE) the dataset.
    """

    def __init__(
        self,
        target_column="Class",
        test_size=0.20,
        random_state=42
    ):
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.numeric_columns = []
        self.categorical_columns = []
        self.preprocessor = None

    def split_dataset(self, df):
        if self.target_column not in df.columns:
            raise ValueError(f"{self.target_column} not found.")
        X = df.drop(columns=[self.target_column])
        df = df.drop_duplicates()
        y = df[self.target_column]

        if len(df) == 0:
            raise ValueError("Dataset is empty.")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            stratify=y,
            random_state=self.random_state
        )
        return X_train, X_test, y_train, y_test

    def identify_columns(self, X):
        # Identify numeric columns (int, float, bool)
        self.numeric_columns = X.select_dtypes(
            include=["int64", "float64", "bool", "int32", "float32"]
        ).columns.tolist()

        # Identify categorical columns (object, category)
        self.categorical_columns = X.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        return self.numeric_columns, self.categorical_columns
    
        print()
        print(
            f"Numeric Features : "
            f"{len(self.numeric_columns)}"
        )
        print(
            f"Categorical Features : "
            f"{len(self.categorical_columns)}"
        )



    def build_pipeline(self):
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", RobustScaler())
            ]
        )

        categorical_pipeline = Pipeline(

            steps=[

                (

                    "imputer",

                    SimpleImputer(

                        strategy="constant",

                        fill_value="Unknown"

                    )

                ),

                (

                    "onehot",

                    OneHotEncoder(

                        handle_unknown="ignore",

                        sparse_output=False

                    )

                )

            ]

        )

        transformers = []
        if self.numeric_columns:
            transformers.append(("numeric", numeric_pipeline, self.numeric_columns))
        if self.categorical_columns:
            transformers.append(("categorical", categorical_pipeline, self.categorical_columns))

        self.preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder="drop"
        )
        return self.preprocessor

    def fit_transform(self, X_train):
        # Ensure ColumnTransformer works with pandas DataFrame
        X_train = self.preprocessor.fit_transform(X_train)
        print(
        f"Training Shape : "
        f"{X_train.shape}"
    )
        return X_train

    def transform(self, X_test):
        X_test = self.preprocessor.transform(

            X_test

        )

        print(

            f"Testing Shape : "

            f"{X_test.shape}"

        )

        return X_test   
        return self.preprocessor.transform(X_test)

    def balance_dataset(self, X_train, y_train):
        print("\nApplying SMOTE...")
        # Clean up target alignment
        if len(np.unique(y_train)) < 2:
            raise ValueError(
                "SMOTE requires two classes."
        )
        
        smote = SMOTE(random_state=self.random_state)
        X_balanced, y_balanced = smote.fit_resample(X_train, y_train)
        print("Dataset Balanced Successfully")
        print(y_balanced.value_counts())
        return X_balanced, y_balanced

    def save_preprocessor(self, filepath="models/preprocessor.joblib"):
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.preprocessor, filepath, compress=3)
        try:

            feature_names = (
                self.preprocessor
                .get_feature_names_out()
            )
            joblib.dump(
                feature_names,
                "models/preprocessor_features.joblib"
            )

        except Exception:
            pass


        print(f"Saved preprocessor -> {filepath}")

    def load_preprocessor(self, filepath="models/preprocessor.joblib"):
        self.preprocessor = joblib.load(filepath)
        return self.preprocessor
