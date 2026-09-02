import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from imblearn.over_sampling import SMOTE


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

    def identify_columns(self, X):
        # Identify numeric columns (int, float, bool)
        self.numeric_columns = X.select_dtypes(
            include=["int64", "float64", "bool", "int32", "float32"]
        ).columns.tolist()

        # Identify categorical columns (object, category, string)
        self.categorical_columns = X.select_dtypes(
            include=["object", "category", "string"]
        ).columns.tolist()

        return self.numeric_columns, self.categorical_columns

    def build_pipeline(self):
        numeric_pipeline = Pipeline(
            steps=[
                ("scaler", RobustScaler())
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
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
        return X_train

    def transform(self, X_test):
        num_cols = getattr(self.preprocessor, "transformers_", [("numeric", None, [])])[0][2]
        cat_cols = getattr(self.preprocessor, "transformers_", [("categorical", None, [])])[1][2] if len(getattr(self.preprocessor, "transformers_", [])) > 1 else []

        # Force exact column ordering as fitted in ColumnTransformer
        all_cols = list(num_cols) + list(cat_cols)
        X_transformed = pd.DataFrame(index=X_test.index)

        for col in num_cols:
            if col in X_test.columns:
                X_transformed[col] = pd.to_numeric(X_test[col], errors="coerce").fillna(0.0).astype(float)
            else:
                X_transformed[col] = 0.0

        for col in cat_cols:
            if col in X_test.columns:
                X_transformed[col] = X_test[col].astype(str).replace(["None", "nan", "NoneType", "np.nan"], "Unknown")
            else:
                X_transformed[col] = "Unknown"

        return self.preprocessor.transform(X_transformed[all_cols])

    def balance_dataset(self, X_train, y_train):
        print("\nApplying SMOTE...")
        # Clean up target alignment
        smote = SMOTE(random_state=self.random_state)
        X_balanced, y_balanced = smote.fit_resample(X_train, y_train)
        print("Dataset Balanced Successfully")
        print(y_balanced.value_counts())
        return X_balanced, y_balanced

    def save_preprocessor(self, filepath="models/preprocessor.joblib"):
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.preprocessor, filepath)
        print(f"Saved preprocessor -> {filepath}")

    def load_preprocessor(self, filepath="models/preprocessor.joblib"):
        self.preprocessor = joblib.load(filepath)
        return self.preprocessor