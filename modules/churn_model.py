# XGBoost training and prediction
# modules/churn_model.py

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

class ChurnModel:
    def __init__(self):
        self.model = None

    def train(self, X, y, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        self.model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"✅ Model trained. Accuracy: {acc:.4f}")
        return self.model

    def predict(self, X_input):
        if self.model is None:
            raise Exception("❌ Model not loaded or trained.")
        return self.model.predict(X_input)

    def save(self, path="models/churn_model.xgb"):
        joblib.dump(self.model, path)
        print(f"✅ Model saved at {path}")

    def load(self, path="models/churn_model.xgb"):
        self.model = joblib.load(path)
        print(f"✅ Model loaded from {path}")
