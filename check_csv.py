import pandas as pd
df = pd.read_csv("data/fraud.csv", nrows=5)
print("Columns:", list(df.columns))
print("Shape of preview:", df.shape)
print(df.head())
