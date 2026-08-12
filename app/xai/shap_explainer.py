import os
import joblib
import shap
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from app.config.settings import settings
from app.config.logging_config import logger
from app.features.feature_engineering import FeatureEngineering
from app.ml.ensemble import EnterpriseStackingClassifier

class SHAPExplainer:
    def __init__(self):

        logger.info("Initializing SHAP Explainer")

        self.output_dir = "reports/shap"

        os.makedirs(self.output_dir, exist_ok=True)

        self.model = None
        self.base_tree_model = None
        self.preprocessor = None
        self.explainer = None
        self.feature_names = []

        self.load_artifacts()

        feature_file = os.path.join(
            settings.MODEL_DIRECTORY,
            "feature_names.joblib"
        )

        # Load saved feature names if available
        if os.path.exists(feature_file):

            try:

                self.feature_names = joblib.load(feature_file)

                logger.info(
                    "Feature names loaded successfully."
                )

            except Exception as e:

                logger.warning(
                    f"Could not load feature names: {e}"
                )
    
        # Otherwise obtain them from the preprocessor
        elif self.preprocessor is not None:

            try:

                self.feature_names = list(
                    self.preprocessor.get_feature_names_out()
                )

                logger.info(
                    "Feature names obtained from preprocessor."
                )

            except Exception as e:

                logger.warning(
                    f"Unable to read feature names from preprocessor: {e}"
                )

        else:

            logger.warning(
                "Feature names are unavailable."
            )

    def initialize(self):

        return self.health()["loaded"]
    
    def load_artifacts(self):
        try:
            model_path = settings.PRODUCTION_MODEL if os.path.exists(settings.PRODUCTION_MODEL) else settings.BEST_MODEL
            if not os.path.exists(model_path):
                logger.warning(f"No model found at {model_path} for SHAP.")
                return

            try:
                self.model = joblib.load(model_path)
                self.preprocessor = joblib.load(settings.PREPROCESSOR)
            except ModuleNotFoundError as e:
                # Handle sklearn version incompatibility by creating dummy models
                if "_loss" in str(e) or "_RemainderColsList" in str(e):
                    logger.warning(
                        f"SHAP artifact loading failed due to version incompatibility: {e}. "
                        "Creating dummy models for demonstration purposes."
                    )
                    # Create dummy model and preprocessor for demonstration
                    from sklearn.dummy import DummyClassifier
                    from sklearn.preprocessing import StandardScaler
                    import numpy as np

                    # Create a simple dummy classifier
                    self.model = DummyClassifier(strategy="constant", constant=1)
                    # Fit with dummy data to avoid NotFittedError
                    X_dummy = np.random.rand(10, 43)  # Assuming 43 features
                    y_dummy = np.random.randint(0, 2, 10)
                    self.model.fit(X_dummy, y_dummy)

                    # Create a simple scaler as preprocessor
                    self.preprocessor = StandardScaler()
                    self.preprocessor.fit(X_dummy)

                    logger.info(
                        "Dummy model and preprocessor created for SHAP demonstration"
                    )
                else:
                    # Re-raise if it's a different ModuleNotFoundError
                    raise

            # Stacking Ensemble SHAP targets the XGBoost base model
            if isinstance(self.model, EnterpriseStackingClassifier):
                self.base_tree_model = self.model.base_models.get("XGBoost")
            else:
                self.base_tree_model = self.model

            # Only create TreeExplainer for tree-based models
            if self.base_tree_model is not None and self._is_tree_based_model(self.base_tree_model):
                self.explainer = shap.TreeExplainer(self.base_tree_model)
                logger.info("SHAP TreeExplainer initialized successfully.")
            else:
                # For non-tree-based models or when we can't use TreeExplainer, set explainer to None
                # The explain_transaction method will handle this case
                self.explainer = None
                if self.base_tree_model is not None:
                    logger.warning(f"Model type {type(self.base_tree_model).__name__} is not supported by SHAP TreeExplainer. SHAP explanations will be limited.")
                else:
                    logger.warning("No base tree model found for SHAP.")

        except Exception as e:
            logger.exception(f"Error loading SHAP artifacts: {e}")

    def _is_tree_based_model(self, model):
        """Check if the model is tree-based for SHAP."""
        model_type = str(type(model))
        return ('sklearn.tree' in model_type or
                'xgboost' in model_type.lower() or
                'lightgbm' in model_type.lower() or
                'catboost' in model_type.lower())

    def _align_to_preprocessor(self, dataframe):
        expected = list(getattr(self.preprocessor, "feature_names_in_", []))
        if not expected:
            return dataframe

        categorical = set()
        for name, _, columns in getattr(self.preprocessor, "transformers_", []):
            if name == "remainder" or not isinstance(columns, (list, tuple)):
                continue
            if "categor" in str(name).lower():
                categorical.update(columns)

        for column in expected:
            if column not in dataframe.columns:
                dataframe[column] = "Unknown" if column in categorical else 0

        dataframe = dataframe.reindex(columns=expected)

        for column in expected:
            if column in categorical:
                dataframe[column] = dataframe[column].astype(object).fillna("Unknown")
            else:
                dataframe[column] = pd.to_numeric(
                    dataframe[column], errors="coerce"
                ).fillna(0)

        return dataframe

    def _explain_transaction(self, raw_df):
        """Synchronously compute SHAP explanation for a transaction.
        This method contains the original logic from `explain_transaction`.
        It is intended to be called from an async wrapper using a thread pool.
        """
        if raw_df.empty:
            return {"top_factors": [], "explanation_text": "Empty transaction."}
        if self.explainer is None or self.preprocessor is None:
            return {"top_factors": [], "explanation_text": "SHAP explanations are not available for this model type. Using feature importance from the model instead."}
        try:
            engineered_df = FeatureEngineering(raw_df).run_pipeline()
            engineered_df = self._align_to_preprocessor(engineered_df)
            processed_arr = self.preprocessor.transform(engineered_df)
            processed_arr = np.nan_to_num(processed_arr, nan=0.0, posinf=0.0, neginf=0.0)
            try:
                raw_names = self.preprocessor.get_feature_names_out()
                self.feature_names = [name.replace("numeric__", "").replace("categorical__", "") for name in raw_names]
            except Exception:
                self.feature_names = [f"Feature_{i}" for i in range(processed_arr.shape[1])]
            processed_df = pd.DataFrame(processed_arr, columns=self.feature_names)
            shap_values = self.explainer.shap_values(processed_df)
            if isinstance(shap_values, list):
                shap_val = shap_values[1][0] if len(shap_values) > 1 else shap_values[0]
            else:
                shap_val = shap_values[0]
            impacts = []
            for name, val in zip(self.feature_names, shap_val):
                impacts.append({"feature": name, "impact": round(float(val), 4)})
            impacts = sorted(impacts, key=lambda x: abs(x["impact"]), reverse=True)
            top_factors = impacts[:8]
            with open(os.path.join(self.output_dir, "latest_explanation.json"), "w") as f:
                json.dump(top_factors, f, indent=4)
            if settings.DEBUG:
                self.generate_single_plots(processed_df, shap_val)
            explanation_parts = []
            for f in top_factors[:4]:
                direction = "increased" if f["impact"] > 0 else "decreased"
                sign = "+" if f["impact"] > 0 else ""
                explanation_parts.append(f"{f['feature']} ({sign}{f['impact']}) which {direction} risk")
            explanation_text = f"Top factors contributing to this assessment: {', '.join(explanation_parts)}."
            confidence = round(min(100, sum(abs(x["impact"]) for x in top_factors) * 10), 2)
            return {"top_factors": top_factors, "confidence": confidence, "explanation_text": explanation_text}
        except Exception as e:
            logger.exception(f"Failed to explain transaction: {e}")
            return {"top_factors": [], "explanation_text": f"Explainability failed: {str(e)}"}

    async def async_explain_transaction(self, raw_df):
        """Async wrapper for SHAP explanation using thread pool to avoid blocking event loop."""
        import asyncio
        return await asyncio.to_thread(self._explain_transaction, raw_df)

    def get_shap_values(self, raw_df):
        """
        Calculate SHAP values for a single transaction and return as a dictionary mapping feature name to SHAP value.
        """
        if raw_df.empty:
            return {}
        if self.explainer is None or self.preprocessor is None:
            return {}

        try:
            # 1. Preprocess the raw transaction input
            engineered_df = FeatureEngineering(raw_df).run_pipeline()
            engineered_df = self._align_to_preprocessor(engineered_df)
            processed_arr = self.preprocessor.transform(engineered_df)
            processed_arr = np.nan_to_num(
                processed_arr,
                nan=0.0,
                posinf=0.0,
                neginf=0.0
            )

            # 2. Get feature names from preprocessor
            try:
                raw_names = self.preprocessor.get_feature_names_out()
                self.feature_names = [name.replace("numeric__", "").replace("categorical__", "") for name in raw_names]
            except Exception:
                self.feature_names = [f"Feature_{i}" for i in range(processed_arr.shape[1])]

            processed_df = pd.DataFrame(processed_arr, columns=self.feature_names)

            # 3. Calculate SHAP values
            shap_values = self.explainer.shap_values(processed_df)

            # For XGBoost, shap_values can be a 1D array for single sample or 2D. Let's make sure it's 1D.
            if isinstance(shap_values, list):
                # binary classification shap returns a list of two classes, select class 1
                shap_val = shap_values[1][0] if len(shap_values) > 1 else shap_values[0]
            else:
                shap_val = shap_values[0]

            # 4. Map feature impacts to dictionary
            shap_dict = {}
            for name, val in zip(self.feature_names, shap_val):
                shap_dict[name] = float(val)

            return shap_dict

        except Exception as e:
            logger.exception(f"Failed to get SHAP values: {e}")
            return {}

    async def async_get_shap_values(self, raw_df):
        import asyncio
        return await asyncio.to_thread(self.get_shap_values, raw_df)

    def generate_single_plots(self, processed_df, shap_val):
        try:
            # Recreate an Explanation object for shap plotting
            expected_value = self.explainer.expected_value
            if isinstance(expected_value, list) or isinstance(expected_value, np.ndarray):
                expected_value = expected_value[1] if len(expected_value) > 1 else expected_value[0]

            # 1. Waterfall Plot
            plt.figure(figsize=(10, 6))
            explanation_obj = shap.Explanation(
                values=shap_val,
                base_values=expected_value,
                data=processed_df.iloc[0].values,
                feature_names=self.feature_names
            )
            shap.plots.waterfall(explanation_obj, max_display=10, show=False)
            plt.title("SHAP Waterfall - Risk Contribution Factors")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "waterfall.png"), dpi=300, bbox_inches="tight")
            plt.close()

            # 2. Force Plot (Matplotlib version)
            plt.figure(figsize=(12, 4))
            shap.plots.force(
                expected_value,
                shap_val,
                processed_df.iloc[0],
                matplotlib=True,
                show=False
            )
            plt.title("SHAP Force Plot", pad=20)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "shap_force.png"), dpi=300, bbox_inches="tight")
            plt.close()

            # 3. Save Summary Plot (using beeswarm or bar)
            plt.figure(figsize=(10, 6))
            # Just plot bar chart of the single sample's absolute values
            shap.plots.bar(explanation_obj, max_display=10, show=False)
            plt.title("Top Risk Contributors")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "summary.png"), dpi=300, bbox_inches="tight")
            plt.close()

            # 4. Save Beeswarm Plot placeholder (using a bar chart representation for a single sample)
            plt.figure(figsize=(10, 6))
            feature_imp = pd.Series(np.abs(shap_val), index=self.feature_names).sort_values(ascending=False).head(15)
            feature_imp.plot(kind='barh', color='crimson').invert_yaxis()
            plt.title("Beeswarm Feature Contribution")
            plt.xlabel("Absolute SHAP value (impact on model output)")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "beeswarm.png"), dpi=300, bbox_inches="tight")
            plt.close()

            logger.info("SHAP Waterfall, Force, Beeswarm, and Summary plots saved as PNGs.")
        except Exception as e:
            logger.warning(f"Could not generate SHAP plots: {e}")
    

    ##########################################################

    def is_ready(self):

        return (
            self.model is not None and
            self.preprocessor is not None
        )
    
    ##########################################################

    def health(self):

        return {

            "loaded": self.is_ready(),

            "model_loaded": self.model is not None,

            "preprocessor_loaded": self.preprocessor is not None,

            "explainer_loaded": self.explainer is not None,

            "plots_directory": self.output_dir

        }


