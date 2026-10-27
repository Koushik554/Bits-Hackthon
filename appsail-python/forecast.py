"""Runs predictions on a DataFrame and applies the switching rules to each row."""
import numpy as np
import pandas as pd

import predict as predict_module
from switching import decide

# Battery rule (document in README):
#  - capacity 500 kWh, starts at 80%, never below 10% or above 100%
#  - Renewable Storage Mode: battery covers 30% of that hour's demand (discharge)
#  - Main Grid Mode: battery charges 40 kWh per hour
BATTERY_KWH = 500.0
SOC_START = 80.0
SOC_MIN = 10.0
SOC_MAX = 100.0
DISCHARGE_SHARE = 0.30
CHARGE_KWH = 40.0


def run_forecast(df: pd.DataFrame) -> list:
    """Return one dict per input row: timestamp, hour, predicted demand, mode, overload."""
    preds = predict_module.predict(df)
    hours = pd.to_datetime(df["timestamp"]).dt.hour.to_numpy()

    temps = df["ambient_temp_c"].to_numpy() if "ambient_temp_c" in df.columns else [0] * len(df)
    humids = df["humidity_pct"].to_numpy() if "humidity_pct" in df.columns else [0] * len(df)
    solars = df["solar_irradiance_wm2"].to_numpy() if "solar_irradiance_wm2" in df.columns else [0] * len(df)

    results = []
    soc = SOC_START
    for ts, hour, demand, temp, hum, sol in zip(df["timestamp"], hours, preds, temps, humids, solars):
        d = decide(float(demand), int(hour))
        if d["mode"] == "Renewable Storage Mode":
            soc -= DISCHARGE_SHARE * float(demand) / BATTERY_KWH * 100
        else:
            soc += CHARGE_KWH / BATTERY_KWH * 100
        soc = max(SOC_MIN, min(SOC_MAX, soc))
        results.append({
            "timestamp": str(ts),
            "hour": int(hour),
            "demand_kw": round(float(demand), 2),
            "mode": d["mode"],
            "overload": d["overload"],
            "battery_soc": round(soc, 1),
            "temp_c": round(float(temp), 1),
            "humidity_pct": round(float(hum), 1),
            "solar_wm2": round(float(sol), 1),
        })
    return results


if __name__ == "__main__":
    import json
    data = pd.read_csv("sample_test_input.csv").head(24)
    print(json.dumps(run_forecast(data)[:3], indent=2))
