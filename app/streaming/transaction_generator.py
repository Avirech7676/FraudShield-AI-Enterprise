import uuid
import pandas as pd


class TransactionGenerator:

    def __init__(self):

        self.df = pd.read_csv("data/raw/creditcard.csv")

        self.index = 0

        print("=" * 60)
        print("REAL DATASET LOADED")
        print(f"Transactions : {len(self.df)}")
        print("=" * 60)

    def generate(self):

        if self.index >= len(self.df):

            self.index = 0

        transaction = self.df.iloc[self.index].to_dict()

        transaction["transaction_id"] = str(uuid.uuid4())

        self.index += 1

        return transaction