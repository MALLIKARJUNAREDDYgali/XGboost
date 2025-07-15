# main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap

from modules.data_processor import DataProcessor
from modules.churn_model import ChurnModel
from modules.shap_explainer import SHAPExplainer

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="ExplainXG - Churn Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# App Title
# ------------------------------
st.title("📊 ExplainXG - XGBoost Churn Explainer")
st.markdown("---")

# ------------------------------
# Session State Init
# ------------------------------
if "model" not in st.session_state:
    st.session_state.model = None
    st.session_state.X = None
    st.session_state.explainer = None

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("🔗 Navigation")
page = st.sidebar.radio("Go to", ["Upload & Train", "Predict & Explain"])

# ------------------------------
# Page 1: Upload & Train
# ------------------------------
if page == "Upload & Train":
    st.header("📁 Upload Dataset")
    uploaded_file = st.file_uploader("Upload Telco Churn CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("🔍 Preview")
            st.dataframe(df.head())

            # Clean and transform
            df_clean = DataProcessor.clean_data(df)
            X, y = DataProcessor.transform(df_clean)

            # Train model
            model = ChurnModel()
            model.train(X, y)
            model.save()

            # SHAP explainer
            explainer = SHAPExplainer(model.model, X)

            # Save to session state
            st.session_state.model = model
            st.session_state.X = X
            st.session_state.explainer = explainer

            st.success("✅ Model trained and explainer ready.")

            # Global SHAP summary
            st.subheader("📊 Global Feature Importance (SHAP Summary)")
            shap_values = explainer.explainer(X)

            fig, ax = plt.subplots(figsize=(10, 6))
            shap.plots.beeswarm(shap_values, show=False)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ------------------------------
# Page 2: Predict & Explain
# ------------------------------
elif page == "Predict & Explain":
    st.header("🧪 Predict Churn for a New Customer")

    if st.session_state.model is None:
        st.warning("⚠️ Please train the model first in 'Upload & Train'")
    else:
        sample = st.session_state.X.iloc[0]

        with st.form("prediction_form"):
            st.subheader("🔧 Enter Customer Info")
            user_input = {}
            for col in sample.index:
                default_val = sample[col]
                input_val = st.text_input(col, str(default_val))
                try:
                    user_input[col] = float(input_val)
                except:
                    user_input[col] = input_val

            submitted = st.form_submit_button("Predict")

        if submitted:
            try:
                input_df = pd.DataFrame([user_input])
                prediction = st.session_state.model.predict(input_df)[0]
                st.success(f"✅ Prediction: {'⚠️ Will Churn' if prediction == 1 else '✅ Will Not Churn'}")

                # SHAP local explanation
                shap_values = st.session_state.explainer.explain_instance(input_df)
                st.subheader("📌 SHAP Explanation (Local)")
                st.write(dict(zip(input_df.columns, shap_values[0].values.tolist())))
            except Exception as e:
                st.error(f"❌ Prediction or explanation failed: {e}")
