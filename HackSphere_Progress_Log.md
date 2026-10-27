# HackSphere 3.0 – Progress Log

**Project:** Smart Energy Microgrid & Demand Forecasting Engine (Zoho Catalyst)
**Time budget:** 2 days (started 2026-10-24)

> Never write real keys, tokens, or secrets in this file.

---

## 1. What we are building

1. Train a regression model in **Catalyst QuickML** to predict `target_demand_kw`.
2. Backend calls the QuickML endpoint for 24 hourly rows and gets 24 predictions.
3. Apply switching rules to each prediction:
   - Demand > 160 kW **or** hour 18–22 inclusive → **Renewable Storage Mode**
   - Otherwise → **Main Grid Mode**
   - Demand ≥ 200 kW → **Critical Overload Alert** (independent of mode)
4. Dashboard (Slate): load curve, grid mode badges, battery state of charge, overload banner.
5. Deploy on Catalyst. Submit: public URL, code (zip or GitHub), working `predict.py`, `README.md`.

**Scoring:** Model RMSE 35% · Deployment 35% · Switching logic 20% · UI 10%.

---

## 2. Data findings

- `train_telemetry.csv`: 4000 rows, hourly, 2014-12-31 → 2015-06-16, no missing values.
- Demand is mostly a step pattern by hour:
  - ~92 kW overnight, ~180 kW at 6–9, ~170 midday, ~205–220 at 18–22, ~115 at 23.
- `hour` is the strongest feature, then temperature, then humidity.
- Test data is likely **later in time** than training → do not use `month` as a feature.
- No lag features (the test input only has weather + timestamp).

---

## 3. Done so far

| # | Step | Status |
|---|------|--------|
| 1 | Inspected data with pandas | Done |
| 2 | Created `train_prepared.csv` (hour, dayofweek + 3 weather cols + target) via `prepare.py` | Done |
| 3 | Uploaded dataset to QuickML | Done |
| 4 | Built **Prediction** pipeline: Source → Random Forest → Destination | Done |
| 5 | Model trained (V2): **RMSE ≈ 11.99, R² ≈ 0.944, MAE ≈ 9.35** | Done |
| 6 | Created endpoint, selected V2, test returned a prediction (~147 kW) | Done |
| 7 | Created Zoho Self Client, obtained OAuth refresh token (scope `QuickML.deployment.READ`) | Done |
| 8 | Rewrote `predict.py` (feature creation, token refresh, CLI `--input/--output`) | Done |
| 9 | Fixed `invalid_client` (bug: values were placed inside `os.getenv()` as the *name*) | Done |
| 10 | `predict.py` now authenticates; first runs **timed out** (30 s, then 60 s read timeouts) | Done (diagnosed) |
| 11 | Diagnosed endpoint: single call = 0.7 s when it answers, but ~4 in 10 calls hang; list (batch) requests also hung | Done |
| 12 | Rewrote `predict.py`: parallel workers (12), short timeout `(5, 4)`, up to 15 retries per row | Done |
| 13 | 20-row check printed sensible predictions (about 90–110 kW overnight, 210–265 kW evening) | Done |
| 14 | Full 1000-row run of `predict.py` + `test_eval.py` | Done |
| 15 | Endpoint returned 403 `PREDICTION_USAGE_LIMIT_EXCEEDED`: free tier allows **500 prediction calls**, all used (hangs + retries burned them) | Done (diagnosed) |
| 16 | Added local fallback: `train_local.py` -> `model_local.joblib` (holdout RMSE ~13.35); `predict.py` probes endpoint once, falls back to local on failure; `test_eval.py` prints SUCCESS | Done |
| 17 | Implemented transition controller in `switching.py` (thresholds: 160 kW, hours 18-22, overload >= 200 kW) with unit test coverage | Done |
| 18 | Built AppSail backend in `app.py` & `forecast.py` with telemetry ingestion, CSV validation, and data cleaning | Done |
| 19 | Built multi-page animated microgrid dashboard (`static/index.html`) using Alpine.js and Chart.js with Overview, Grid Modes, Battery SoC, and Hourly Log | Done |
| 20 | Deployed live onto Zoho Catalyst AppSail via CLI (`catalyst deploy`) | Done |
| 21 | Generated comprehensive `README.md` with system architecture, BESS simulation rules, and setup instructions | Done |

---

## 4. Key learnings / gotchas

- **Pipeline type:** choose *Prediction* (Classic builder), not Time Series Forecasting.
- **Pipeline wiring:** nodes only count when connected on both sides (Source → model → Destination). Orange badge = node not configured.
- **Endpoint 500 `PREDICTION_FAILED`:** was fixed by re-executing the pipeline (new version V2) and selecting V2 on the endpoint, then Update/Publish.
- **Training and inference features must match:** `hour` and `dayofweek` are computed from `timestamp` in `predict.py` exactly as in `prepare.py`.
- **`os.getenv(NAME, default)`:** first argument is the variable *name*; the real value goes only as the default (second argument).
- **OAuth:** the one-time code expires in 10 minutes; the access token lasts 1 hour; the refresh token is long-lived. `predict.py` fetches a fresh access token on every run.
- **Request format that works:** `{"data": {"hour": 17, "dayofweek": 0, "ambient_temp_c": 30.5, "humidity_pct": 62.21, "solar_irradiance_wm2": 40}}` → `{"result": [147.14...]}`
- **Required headers:** `X-QUICKML-ENDPOINT-KEY`, `Authorization: Zoho-oauthtoken <token>`, `CATALYST-ORG`, `Environment: Development`.
- **Endpoint hangs intermittently:** about 40% of calls never answer (ReadTimeout) while the rest return in under 1.5 s. It is not rate limiting. Fix: give up on a call after ~4 s and retry, run several workers in parallel so a hung call only blocks one.
- **Batching:** list-of-rows requests (5 and 50 rows) both hung, so assume only single-row requests work unless a retest proves otherwise.
- **Where training lives:** the model is trained in Catalyst QuickML (Datasets → Pipelines → Models → Endpoints), not on the laptop. `predict.py` only sends rows to the endpoint.
- **Security:** keep keys out of public repos and out of chat. After the hackathon, delete the Self Client and regenerate the endpoint key.

---

## 5. Commands

```bash
# create training file for QuickML
python prepare.py

# run predictions locally
python predict.py --input sample_test_input.csv --output predictions.csv

# mandatory pre-submission check (must print SUCCESS)
python test_eval.py
```

Install libraries (if `pip` launcher is broken on Windows):

```bash
python -m pip install pandas numpy requests
```

---

## 6. Current status / risk

`predict.py` now works on a 20-row sample. The full 1000-row run and `test_eval.py` still need to be run (expected 3–5 minutes each).

**Risk:** the endpoint intermittently hangs. The organizers run `predict.py` against it for the hidden test, so a flaky endpoint could hurt the 35% accuracy score.

**Mitigations:**
1. Tell the organizers (support channel) that the QuickML endpoint intermittently hangs.
2. If time allows, retrain with CatBoost / Gradient Boosting, publish a second endpoint, and rerun `test_batch.py`. If the new endpoint does not hang, switch `predict.py` to it and keep the Random Forest endpoint as backup.
3. If a run crashes after all retries, run it again or lower `max_workers` to 6.

---

## 7. Next steps (Submission Checklist)

1. [x] Full run: `predict.py` writes 1000 predictions, `test_eval.py` prints `SUCCESS`
2. [x] Write switching logic function (Main Grid / Renewable Storage / overload)
3. [x] Backend (Catalyst AppSail): upload CSV or JSON -> predictions + modes + SoC
4. [x] Deploy backend on Zoho Catalyst AppSail and obtain public URL
5. [x] Dashboard: load curve, mode badges, overload banner, battery SoC, multi-page navigation
6. [x] Battery SoC simulation (documented in `README.md` and `forecast.py`)
7. [x] Data cleaning for uploads (handling missing values, invalid timestamps)
8. [x] `README.md`: setup, architecture, environment variables, BESS logic
9. [ ] Copy public Catalyst AppSail URL into `README.md`
10. [ ] Create submission zip (`TeamName_Submission.zip`) or push to GitHub and submit!

**Optional, if time remains:** try CatBoost / gradient boosting for lower RMSE; add an `is_evening` feature (must be added in `predict.py` too); drop `dayofweek` (near-zero importance).

---

## 8. Files in the project folder

| File | Purpose |
|------|---------|
| `train_telemetry.csv` | Original training data |
| `train_prepared.csv` | Features used to train in QuickML |
| `prepare.py` | Builds `train_prepared.csv` |
| `predict.py` | Calls the QuickML endpoint, writes `predictions.csv` |
| `test_eval.py` | Organizer self-check |
| `get_token.py` | One-time token script — **delete, never submit** |
| `test_endpoint.py` | Times a single endpoint call (diagnostic, optional to submit) |
| `test_batch.py` | Tests sequential vs batch requests (diagnostic, optional to submit) |
