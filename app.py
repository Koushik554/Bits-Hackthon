"""Flask backend: upload a CSV, get forecasts + switching decisions as JSON."""
import io
import os

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

from forecast import run_forecast

app = Flask(__name__, static_folder="static", static_url_path="/static")

REQUIRED = ["timestamp", "ambient_temp_c", "humidity_pct", "solar_irradiance_wm2"]
NUMERIC = ["ambient_temp_c", "humidity_pct", "solar_irradiance_wm2"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with bad timestamps, coerce numbers, fill gaps."""
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].fillna(df[c].median()) if df[c].notna().any() else df[c].fillna(0)
    if df.empty:
        raise ValueError("No valid rows after cleaning")
    return df


@app.get("/")
def index():
    resp = send_from_directory("static", "index.html")
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


def _respond(results):
    return jsonify({
        "count": len(results),
        "overload_count": sum(r["overload"] for r in results),
        "results": results,
    })


@app.get("/api/sample")
def sample():
    """Forecast the first N rows (default 24) of the bundled sample file."""
    n = request.args.get("n", default=24, type=int)
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_test_input.csv")).head(n)
        return _respond(run_forecast(clean(df)))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.post("/api/forecast")
def forecast():
    try:
        if "file" in request.files:
            df = pd.read_csv(io.BytesIO(request.files["file"].read()))
        elif request.is_json:
            df = pd.DataFrame(request.get_json())
        else:
            return jsonify({"error": "Send a CSV as form field 'file' or a JSON list of rows"}), 400
        results = run_forecast(clean(df))
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({
        "count": len(results),
        "overload_count": sum(r["overload"] for r in results),
        "results": results,
    })


if __name__ == "__main__":
    port = int(os.getenv("X_ZOHO_CATALYST_LISTEN_PORT", os.getenv("PORT", "9000")))
    app.run(host="0.0.0.0", port=port)
