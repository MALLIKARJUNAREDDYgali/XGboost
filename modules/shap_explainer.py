# SHAP explanations
# modules/shap_explainer.py

import shap

class SHAPExplainer:
    def __init__(self, model, background_data):
        self.model = model
        self.explainer = shap.Explainer(self.model, background_data)

    def explain_instance(self, input_data):
        shap_values = self.explainer(input_data)
        return shap_values

    def plot_local_explanation(self, shap_values, index=0):
        shap.plots.force(shap_values[index])

    def plot_summary(self, shap_values):
        shap.plots.beeswarm(shap_values)
