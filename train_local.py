"""Trains a local fallback model on train_prepared.csv (same features as the QuickML model)."""
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

FEATURES = ["hour", "dayofweek", "ambient_temp_c", "humidity_pct", "solar_irradiance_wm2"]

df = pd.read_csv("train_prepared.csv")
X, y = df[FEATURES], df["target_demand_kw"]

# Time-ordered holdout (test data is later in time than training data)
cut = int(len(df) * 0.8)
m = RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=0, n_jobs=-1)
m.fit(X[:cut], y[:cut])
rmse = np.sqrt(mean_squared_error(y[cut:], m.predict(X[cut:])))
print(f"Holdout RMSE: {rmse:.2f}")

m.fit(X, y)
joblib.dump(m, "model_local.joblib")
print("Saved model_local.joblib")
