import os
import pandas as pd


class DataLoader:
    """
    Enterprise Data Loader

    Supports:
    - CSV
    - Excel (.xlsx, .xls)

    Performs:
    - Validation
    - Missing Value Analysis
    - Duplicate Detection
    - Dataset Summary
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None

    ##########################################################

    def validate_file(self):

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"\nDataset not found:\n{self.filepath}"
            )

        extension = os.path.splitext(self.filepath)[1].lower()

        if extension not in [".csv", ".xlsx", ".xls"]:
            raise ValueError(
                f"Unsupported file format: {extension}"
            )

    ##########################################################

    def load_dataset(self):

        self.validate_file()

        extension = os.path.splitext(self.filepath)[1].lower()

        print("=" * 70)
        print("LOADING DATASET")
        print("=" * 70)

        if extension == ".csv":
            self.df = pd.read_csv(self.filepath)

        else:
            self.df = pd.read_excel(self.filepath)

        print(f"\nDataset Loaded Successfully")
        print(f"Shape : {self.df.shape}")

        return self.df

    ##########################################################

    def dataset_info(self):

        print("\n")
        print("=" * 70)
        print("DATASET INFORMATION")
        print("=" * 70)

        print(self.df.info())

    ##########################################################

    def preview(self, rows=5):

        print("\n")
        print("=" * 70)
        print("FIRST RECORDS")
        print("=" * 70)

        print(self.df.head(rows))

    ##########################################################

    def check_missing_values(self):

        print("\n")
        print("=" * 70)
        print("MISSING VALUES")
        print("=" * 70)

        missing = self.df.isnull().sum()

        missing = missing[missing > 0]

        if len(missing) == 0:

            print("No Missing Values Found")

        else:

            print(missing)

    ##########################################################

    def check_duplicates(self):

        print("\n")
        print("=" * 70)
        print("DUPLICATE RECORDS")
        print("=" * 70)

        duplicates = self.df.duplicated().sum()

        print(f"Duplicate Rows : {duplicates}")

    ##########################################################

    def statistical_summary(self):

        print("\n")
        print("=" * 70)
        print("STATISTICAL SUMMARY")
        print("=" * 70)

        print(self.df.describe(include="all"))

    ##########################################################

    def target_distribution(self, target_column="Class"):

        if target_column not in self.df.columns:
            return

        print("\n")
        print("=" * 70)
        print("TARGET DISTRIBUTION")
        print("=" * 70)

        print(self.df[target_column].value_counts())

        print("\nPercentage")

        print(
            self.df[target_column]
            .value_counts(normalize=True) * 100
        )

    ##########################################################

    def profile(self):

        """
        Complete dataset profiling
        """

        self.dataset_info()

        self.preview()

        self.check_missing_values()

        self.check_duplicates()

        self.statistical_summary()

        self.target_distribution()