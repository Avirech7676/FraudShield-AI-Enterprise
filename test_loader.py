from app.utils.data_loader import DataLoader

loader = DataLoader("data/raw/creditcard.csv")

df = loader.load_dataset()

loader.profile()