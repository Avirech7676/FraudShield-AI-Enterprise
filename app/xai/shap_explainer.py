import os
import joblib
import shap
import matplotlib.pyplot as plt

class SHAPExplainer:

    def __init__(self):
        print("Loading model...")
        self.model = joblib.load("models/best_model.joblib")

        print("Creating SHAP Explainer...")
        self.explainer = shap.TreeExplainer(self.model)

        self.output_dir = "reports/shap"
        os.makedirs(self.output_dir, exist_ok=True)

    ##################################################

    def explain(self, X):
        print(f"Generating SHAP values for {len(X)} samples...")
        shap_values = self.explainer.shap_values(X)
        print("SHAP values generated successfully.")
        return shap_values

    ##################################################

    def summary_plot(self, X):
        shap_values = self.explain(X)

        plt.figure()
        shap.summary_plot(
            shap_values,
            X,
            show=False
        )

        plt.savefig(
            os.path.join(self.output_dir, "summary_plot.png"),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()
        print("Summary Plot Saved")

    ##################################################

    def bar_plot(self, X):
        shap_values = self.explain(X)

        plt.figure()
        shap.summary_plot(
            shap_values,
            X,
            plot_type="bar",
            show=False
        )

        plt.savefig(
            os.path.join(self.output_dir, "bar_plot.png"),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()
        print("Bar Plot Saved")

    ##################################################

    def feature_importance_plot(self, X):
        print("Generating SHAP values...")
        shap_values = self.explainer.shap_values(X)
        print("SHAP values generated successfully.")

        plt.figure(figsize=(10, 6))
        shap.summary_plot(
            shap_values,
            X,
            plot_type="bar",
            show=False
        )
        plt.tight_layout()

        plt.savefig(
            os.path.join(self.output_dir, "feature_importance.png"),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()
        print("Feature Importance Plot Saved")

    ##################################################

    def waterfall_plot(self, X):
        print("Generating Waterfall Plot...")

        explanation = self.explainer(X.iloc[:1])

        plt.figure(figsize=(10, 6))
        shap.plots.waterfall(
            explanation[0],
            show=False
        )

        plt.savefig(
            os.path.join(self.output_dir, "waterfall_plot.png"),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()
        print("Waterfall Plot Saved")

    ##################################################

    def decision_plot(self, X):
        print("Generating Decision Plot...")

        explanation = self.explainer(X.iloc[:100])

        plt.figure(figsize=(12, 8))
        shap.decision_plot(
            self.explainer.expected_value,
            explanation.values,
            X.iloc[:100],
            show=False
        )

        plt.savefig(
            os.path.join(self.output_dir, "decision_plot.png"),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()
        print("Decision Plot Saved")

    ##################################################

    def force_plot(self, X):
        print("Generating Force Plot...")

        explanation = self.explainer(X.iloc[:1])
        force = shap.plots.force(
            explanation[0],
            matplotlib=False
        )

        shap.save_html(
            os.path.join(self.output_dir, "force_plot.html"),
            force
        )

        print("Force Plot Saved")
    