import pandas as pd

df = pd.read_csv("train_telemetry.csv", parse_dates=["timestamp"])
print(df.describe())
print(df.isna().sum())
print(df.groupby(df.timestamp.dt.hour).target_demand_kw.mean().round(1))