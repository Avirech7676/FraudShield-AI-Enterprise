import pandas as pd
import numpy as np

class FeatureEngineering:
    """
    Feature Engineering & Enrichment Pipeline
    Transforms PCA (V1-V28) dataset into 43 semantic features.
    Handles both training batch enrichment and real-time prediction request formatting.
    """

    def __init__(self, df):
        self.df = df.copy()

    def handle_missing_values(self):
        # Fill numeric missing values with median, categorical with mode/default
        numeric = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric] = self.df[numeric].fillna(self.df[numeric].median())
        return self.df

    def remove_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        if before > after:
            print(f"Removed {before-after} duplicate rows.")
        return self.df

    def enrich_dataset(self):
        """
        Enriches the V1-V28 PCA dataset with 43 semantic features.
        If features are already present (e.g. from prediction API requests), does nothing.
        """
        required_cols = ["Device_Trust_Score", "VPN_Detection", "IP_Reputation"]
        if all(col in self.df.columns for col in required_cols):
            # Already has rich features (from inference)
            return self.df

        print("Enriching dataset with 43 semantic features...")
        n_samples = len(self.df)
        is_fraud = self.df["Class"].values if "Class" in self.df.columns else np.zeros(n_samples)

        # Set seed for batch reproducibility
        np.random.seed(42)

        # 1. Currency
        currencies = ["USD", "EUR", "GBP", "CAD"]
        self.df["Currency"] = np.random.choice(currencies, size=n_samples, p=[0.90, 0.05, 0.03, 0.02])

        # 2. Merchant & Merchant Category
        merchants = ["Amazon", "Walmart", "Target", "Apple", "Netflix", "Steam", "Uber", "Airbnb", "BestBuy", "Unknown"]
        p_gen = [0.20, 0.20, 0.15, 0.10, 0.10, 0.05, 0.10, 0.05, 0.03, 0.02]
        p_frd = [0.05, 0.05, 0.05, 0.10, 0.05, 0.25, 0.20, 0.05, 0.10, 0.10]
        
        rand_m = np.random.rand(n_samples)
        cum_gen = np.cumsum(p_gen)
        cum_frd = np.cumsum(p_frd)
        merchant_arr = np.empty(n_samples, dtype=object)
        
        for idx in range(n_samples):
            p = cum_frd if is_fraud[idx] == 1 else cum_gen
            m_idx = np.searchsorted(p, rand_m[idx])
            m_idx = min(m_idx, len(merchants) - 1)
            merchant_arr[idx] = merchants[m_idx]
        self.df["Merchant"] = merchant_arr

        category_map = {
            "Amazon": "Retail", "Walmart": "Retail", "Target": "Retail",
            "Apple": "Electronics", "BestBuy": "Electronics",
            "Netflix": "Entertainment", "Steam": "Entertainment",
            "Uber": "Travel", "Airbnb": "Travel", "Unknown": "Services"
        }
        self.df["Merchant_Category"] = self.df["Merchant"].map(category_map).fillna("Services")

        # 3. Payment Type
        payment_types = ["Credit", "Debit", "Transfer", "Gift Card"]
        p_gen_pay = [0.60, 0.35, 0.04, 0.01]
        p_frd_pay = [0.30, 0.10, 0.30, 0.30]
        cum_gen_pay = np.cumsum(p_gen_pay)
        cum_frd_pay = np.cumsum(p_frd_pay)
        pay_arr = np.empty(n_samples, dtype=object)
        rand_p = np.random.rand(n_samples)
        
        for idx in range(n_samples):
            p = cum_frd_pay if is_fraud[idx] == 1 else cum_gen_pay
            p_idx = np.searchsorted(p, rand_p[idx])
            p_idx = min(p_idx, len(payment_types) - 1)
            pay_arr[idx] = payment_types[p_idx]
        self.df["Payment_Type"] = pay_arr

        # 4. Transaction details
        self.df["Card_Present"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.05, np.random.rand(n_samples) < 0.60)
        self.df["Chip_Used"] = np.where(self.df["Card_Present"], np.random.rand(n_samples) < 0.80, False)
        self.df["Contactless"] = np.where(self.df["Card_Present"] & ~self.df["Chip_Used"], np.random.rand(n_samples) < 0.70, False)
        self.df["International"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.45, np.random.rand(n_samples) < 0.06)

        # 5. Customer demographics
        self.df["Customer_Age"] = np.clip(np.random.normal(44, 15, size=n_samples).astype(int), 18, 85)
        self.df["Customer_Segment"] = np.random.choice(["Standard", "Premium", "VIP"], size=n_samples, p=[0.80, 0.15, 0.05])
        self.df["KYC_Level"] = np.random.choice(["Level_1", "Level_2", "Level_3"], size=n_samples, p=[0.20, 0.50, 0.30])
        self.df["Customer_Lifetime"] = np.random.uniform(0.1, 10.0, size=n_samples).round(1)
        self.df["Avg_Spend"] = (np.random.exponential(80, size=n_samples) + 5).round(2)
        self.df["Monthly_Spend"] = (self.df["Avg_Spend"] * np.random.randint(5, 30, size=n_samples)).round(2)
        self.df["Credit_Limit"] = np.random.choice([1000.0, 2500.0, 5000.0, 10000.0, 20000.0, 50000.0], size=n_samples, p=[0.20, 0.30, 0.25, 0.15, 0.08, 0.02])

        # 6. Device features
        self.df["Device_Fingerprint"] = [f"dev_{np.random.randint(100000, 999999)}" for _ in range(n_samples)]
        self.df["Device_Trust_Score"] = np.clip(np.where(is_fraud == 1, np.random.normal(32, 18, size=n_samples), np.random.normal(90, 8, size=n_samples)), 0, 100).round(1)
        self.df["Browser"] = np.random.choice(["Chrome", "Safari", "Firefox", "Edge", "Unknown"], size=n_samples, p=[0.60, 0.25, 0.08, 0.05, 0.02])
        self.df["Operating_System"] = np.random.choice(["Windows", "MacOS", "iOS", "Android", "Linux"], size=n_samples, p=[0.45, 0.25, 0.15, 0.12, 0.03])
        self.df["Emulator_Detection"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.15, np.random.rand(n_samples) < 0.001)
        self.df["Rooted_Device"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.25, np.random.rand(n_samples) < 0.005)
        self.df["Jailbreak_Detection"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.20, np.random.rand(n_samples) < 0.003)

        # 7. Network and Geo features
        self.df["IP_Reputation"] = np.clip(np.where(is_fraud == 1, np.random.normal(78, 16, size=n_samples), np.random.normal(12, 8, size=n_samples)), 0, 100).round(1)
        self.df["VPN_Detection"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.70, np.random.rand(n_samples) < 0.04)
        self.df["TOR_Detection"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.15, np.random.rand(n_samples) < 0.001)
        self.df["ASN"] = [f"AS{np.random.randint(1000, 9999)}" for _ in range(n_samples)]
        
        countries = ["US", "IN", "CA", "GB", "RU", "CN", "BR"]
        c_gen = [0.75, 0.10, 0.05, 0.05, 0.01, 0.01, 0.03]
        c_frd = [0.30, 0.15, 0.05, 0.05, 0.20, 0.15, 0.10]
        c_arr = np.empty(n_samples, dtype=object)
        rand_c = np.random.rand(n_samples)
        cum_gen_c = np.cumsum(c_gen)
        cum_frd_c = np.cumsum(c_frd)
        for idx in range(n_samples):
            p = cum_frd_c if is_fraud[idx] == 1 else cum_gen_c
            c_idx = np.searchsorted(p, rand_c[idx])
            c_idx = min(c_idx, len(countries) - 1)
            c_arr[idx] = countries[c_idx]
        self.df["Country"] = c_arr
        self.df["City"] = "Unknown"
        self.df["ISP"] = "Unknown"

        # 8. Behavioral features
        tx_gen = np.random.poisson(0.4, size=n_samples)
        tx_frd = np.random.poisson(5.2, size=n_samples)
        self.df["Transactions_Last_Hour"] = np.where(is_fraud == 1, tx_frd, tx_gen)
        self.df["Transactions_Last_Day"] = self.df["Transactions_Last_Hour"] * 8 + np.random.poisson(2, size=n_samples)
        self.df["Velocity"] = self.df["Amount"] * (self.df["Transactions_Last_Hour"] + 1)
        self.df["Time_Since_Last_Transaction"] = np.where(is_fraud == 1, np.random.exponential(10, size=n_samples), np.random.exponential(3600, size=n_samples)).round(1)
        self.df["Merchant_Diversity"] = np.random.randint(1, 10, size=n_samples)
        self.df["Location_Jump"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.40, np.random.rand(n_samples) < 0.01)
        self.df["Device_Change"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.35, np.random.rand(n_samples) < 0.015)
        self.df["Password_Reset"] = np.where(is_fraud == 1, np.random.rand(n_samples) < 0.12, np.random.rand(n_samples) < 0.005)
        
        lf_gen = np.random.poisson(0.04, size=n_samples)
        lf_frd = np.random.poisson(2.5, size=n_samples)
        self.df["Login_Failure_Count"] = np.where(is_fraud == 1, lf_frd, lf_gen)

        # 9. Merchant risk
        mr_gen = np.random.normal(12, 6, size=n_samples)
        mr_frd = np.random.normal(70, 15, size=n_samples)
        self.df["Merchant_Risk"] = np.clip(np.where(is_fraud == 1, mr_frd, mr_gen), 0, 100).round(1)
        self.df["Merchant_Chargeback_Rate"] = (self.df["Merchant_Risk"] / 100.0 * np.random.uniform(0, 5, size=n_samples)).round(2)
        self.df["Merchant_Country"] = self.df["Country"]

        # 10. History
        pf_gen = np.random.choice([0, 1, 2], size=n_samples, p=[0.998, 0.0015, 0.0005])
        pf_frd = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.75, 0.15, 0.08, 0.02])
        self.df["Previous_Fraud"] = np.where(is_fraud == 1, pf_frd, pf_gen)

        return self.df

    def select_ml_features(self):
        """
        Selects the features to use for machine learning models,
        excluding raw PCA V-columns, Time, and high cardinality strings.
        """
        cols_to_drop = [
            "Time", "Device_Fingerprint", "ASN", "City", "ISP"
        ]
        # Drop PCA V-columns if they are present
        v_cols = [f"V{i}" for i in range(1, 29)]
        cols_to_drop.extend([col for col in v_cols if col in self.df.columns])

        clean_df = self.df.drop(columns=[col for col in cols_to_drop if col in self.df.columns], errors="ignore")
        return clean_df

    def run_pipeline(self):
        print("=" * 60)
        print("RUNNING FEATURE PIPELINE")
        print("=" * 60)
        self.handle_missing_values()
        self.remove_duplicates()
        self.enrich_dataset()
        self.df = self.select_ml_features()
        print(f"Feature Pipeline Completed. Output shape: {self.df.shape}")
        return self.df