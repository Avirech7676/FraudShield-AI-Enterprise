import pandas as pd


def load_dataset():

    path = "data/raw/creditcard.csv"

    df = pd.read_csv(path)

    print("=" * 60)
    print("Dataset Loaded Successfully")
    print("=" * 60)
    print("Shape :", df.shape)
    print("Missing Values")
    print(df.isnull().sum())
    print("\nClass Distribution")
    print(df["Class"].value_counts())

    return df