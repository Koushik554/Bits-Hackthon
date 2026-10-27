import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import requests

ENDPOINT_URL = os.getenv(
    "QUICKML_ENDPOINT_URL",
    "https://api.catalyst.zoho.in/quickml/v1/project/102860000000013050/endpoints/predict",
)
ENDPOINT_KEY = os.getenv("QUICKML_ENDPOINT_KEY", "")
CATALYST_ORG = os.getenv("CATALYST_ORG", "60093274698")
CLIENT_ID = os.getenv("ZOHO_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET", "")
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN", "")

FEATURES = ["hour", "dayofweek", "ambient_temp_c", "humidity_pct", "solar_irradiance_wm2"]


def get_access_token():
    if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
        raise ValueError("Zoho OAuth credentials not set; using local model")
    r = requests.post(
        "https://accounts.zoho.in/oauth/v2/token",
        data={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
        },
        timeout=30,
    )
    body = r.json()
    if "access_token" not in body:
        raise RuntimeError(f"Token request failed: {body}")
    return body["access_token"]


def _predict_one(row, headers, retries=15):
    last = None
    for attempt in range(retries):
        try:
            r = requests.post(
                ENDPOINT_URL, json={"data": row}, headers=headers, timeout=(5, 4)
            )
            if r.status_code == 200:
                return float(r.json()["result"][0])
            last = f"HTTP {r.status_code}: {r.text[:200]}"
            if "USAGE_LIMIT_EXCEEDED" in r.text:
                # Quota is exhausted: retrying cannot help and only wastes requests.
                raise RuntimeError(f"Endpoint quota exceeded. {last}")
            if r.status_code in (403, 429):
                time.sleep(2 + attempt)
        except RuntimeError:
            raise
        except Exception as e:
            last = type(e).__name__
        time.sleep(0.3)
    raise RuntimeError(f"Row failed after {retries} tries. Last error: {last}")


def predict(input_df: pd.DataFrame):
    df = input_df.copy()
    ts = pd.to_datetime(df["timestamp"])
    df["hour"] = ts.dt.hour
    df["dayofweek"] = ts.dt.dayofweek
    for c in ["ambient_temp_c", "humidity_pct", "solar_irradiance_wm2"]:
        df[c] = df[c].fillna(df[c].median())

    records = df[FEATURES].to_dict(orient="records")
    if not records:
        return np.array([], dtype=float)
    try:
        headers = {
            "X-QUICKML-ENDPOINT-KEY": ENDPOINT_KEY,
            "Authorization": f"Zoho-oauthtoken {get_access_token()}",
            "CATALYST-ORG": CATALYST_ORG,
            "Environment": "Development",
            "Content-Type": "application/json",
        }
        first = _predict_one(records[0], headers)  # probe: 1 request
        with ThreadPoolExecutor(max_workers=4) as pool:
            rest = list(pool.map(lambda row: _predict_one(row, headers), records[1:]))
        return np.array([first] + rest, dtype=float)
    except Exception as e:
        print(f"Endpoint unavailable ({e}); using local fallback model")
        return _predict_local(df)


_LOCAL_MODEL = None


def _predict_local(df):
    global _LOCAL_MODEL
    if _LOCAL_MODEL is None:
        here = os.path.dirname(os.path.abspath(__file__))
        try:
            import joblib
            _LOCAL_MODEL = joblib.load(os.path.join(here, "model_local.joblib"))
        except Exception:
            # Pickle missing/incompatible with this Python or sklearn version: retrain (takes seconds)
            from sklearn.ensemble import RandomForestRegressor
            train = pd.read_csv(os.path.join(here, "train_prepared.csv"))
            _LOCAL_MODEL = RandomForestRegressor(
                n_estimators=300, min_samples_leaf=3, random_state=0, n_jobs=-1
            ).fit(train[FEATURES], train["target_demand_kw"])
    return np.array(_LOCAL_MODEL.predict(df[FEATURES]), dtype=float)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="sample_test_input.csv")
    parser.add_argument("--output", default="predictions.csv")
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    preds = predict(data)
    out = pd.DataFrame({"timestamp": data["timestamp"], "target_demand_kw": np.round(preds, 2)})
    out.to_csv(args.output, index=False)
    print(f"Wrote {len(out)} predictions to {args.output}")