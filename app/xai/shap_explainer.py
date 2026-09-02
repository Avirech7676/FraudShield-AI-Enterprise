import os
import joblib
import shap
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

    def load_artifacts(self):
        try:
            model_path = settings.PRODUCTION_MODEL if os.path.exists(settings.PRODUCTION_MODEL) else settings.BEST_MODEL
            if not os.path.exists(model_path):
                logger.warning(f"No model found at {model_path} for SHAP.")
                return

            self.model = joblib.load(model_path)
            self.preprocessor = joblib.load(settings.PREPROCESSOR)
            
            # Stacking Ensemble SHAP targets the XGBoost base model
            if isinstance(self.model, EnterpriseStackingClassifier):
                self.base_tree_model = self.model.base_models.get("XGBoost")
            else:
                self.base_tree_model = self.model

            if self.base_tree_model is not None:
                self.explainer = shap.TreeExplainer(self.base_tree_model)
                logger.info("SHAP TreeExplainer initialized successfully.")
            else:
                logger.warning("No base tree model found for SHAP.")
        except Exception as e:
            logger.exception(f"Error loading SHAP artifacts: {e}")

    def explain_transaction(self, raw_df):
        """
        Calculates SHAP values for a single transaction.
        Returns:
            dict containing:
                - top_factors: list of dicts (feature, impact)
                - explanation_text: natural language explanation
        """
        if self.explainer is None or self.preprocessor is None:
            return {"top_factors": [], "explanation_text": "SHAP Explainer not initialized."}

        try:
            # 1. Preprocess the raw transaction input using DataPreprocessor wrapper
            engineered_df = FeatureEngineering(raw_df).run_pipeline()
            from app.ml.preprocessing import DataPreprocessor
            dp = DataPreprocessor()
            dp.preprocessor = self.preprocessor
            processed_arr = dp.transform(engineered_df)
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

            # 4. Map feature impacts
            impacts = []
            for name, val in zip(self.feature_names, shap_val):
                impacts.append({
                    "feature": name,
                    "impact": round(float(val), 4)
                })

            # Sort by absolute impact
            impacts = sorted(impacts, key=lambda x: abs(x["impact"]), reverse=True)
            top_factors = impacts[:10]  # Get top 10 factors

            # 5. Generate plots dynamically for this single transaction
            self.generate_single_plots(processed_df, shap_val)

            # 6. Generate natural language explanation
            explanation_parts = []
            for f in top_factors[:4]:
                direction = "increased" if f["impact"] > 0 else "decreased"
                sign = "+" if f["impact"] > 0 else ""
                explanation_parts.append(f"{f['feature']} ({sign}{f['impact']}) which {direction} risk")
            
            explanation_text = f"Top factors contributing to this assessment: {', '.join(explanation_parts)}."

            return {
                "top_factors": top_factors,
                "explanation_text": explanation_text
            }

        except Exception as e:
            logger.exception(f"Failed to explain transaction: {e}")
            return {"top_factors": [], "explanation_text": f"Explainability failed: {str(e)}"}

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
