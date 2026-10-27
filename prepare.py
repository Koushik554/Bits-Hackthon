import pandas as pd

df = pd.read_csv("train_telemetry.csv", parse_dates=["timestamp"])
df["hour"] = df.timestamp.dt.hour
df["dayofweek"] = df.timestamp.dt.dayofweek

cols = ["hour", "dayofweek", "ambient_temp_c", "humidity_pct",
        "solar_irradiance_wm2", "target_demand_kw"]
df[cols].to_csv("train_prepared.csv", index=False)
print(df[cols].head())