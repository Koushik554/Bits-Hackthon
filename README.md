# HackSphere 3.0: Smart Energy Microgrid & Demand Forecasting Engine

An end-to-end intelligent microgrid demand forecasting and energy transition engine deployed on **Zoho Catalyst (AppSail + QuickML)**.

---

## 1. Live Deployment & Architecture

- **Platform:** Zoho Catalyst AppSail (Python 3.9 Managed Runtime) + QuickML
- **Live Application URL:** *[Insert your Catalyst AppSail Deployment URL here]*
- **Evaluation Status:** `test_eval.py` verified with `SUCCESS`

### System Architecture

```mermaid
flowchart TD
    A[Telemetry Ingestion / CSV Upload / Form] --> B[AppSail Backend (Flask API)]
    B --> C[Feature Engineering (Hour, DayOfWeek, Temp, Humidity, Solar)]
    C --> D[Predictive Forecasting Engine]
    D -.->|Primary| E[Zoho Catalyst QuickML Endpoint]
    D -.->|High-Availability Fallback| F[Trained Local RF Ensemble (RMSE ~13.3)]
    D --> G[Predicted Hourly Demand kW]
    G --> H[Transition Controller (switching.py)]
    H --> I[Renewable Storage Mode vs. Main Grid Mode]
    H --> J[Critical Overload Alert Engine (>=200 kW)]
    I & J --> K[BESS SoC Simulation (500 kWh Battery)]
    K --> L[Interactive Multi-Page Dashboard (Alpine.js + Chart.js)]
```

---

## 2. Transition Controller & Switching Logic

The microgrid dispatch controller (`switching.py`) dynamically assigns operational states for each forecast hour:

| Condition | Microgrid State | Action Taken |
| :--- | :--- | :--- |
| **Demand > 160 kW** OR **Hour in [18:00, 22:00]** | **Renewable Storage Mode** | Discharges local BESS battery to shave peak load and protect grid stability. |
| **Demand $\le$ 160 kW** AND **Hour outside [18, 22]** | **Main Grid Mode** | Draws baseline power from utility grid; recharges local BESS reserves. |
| **Demand $\ge$ 200 kW** | **Critical Overload Alert** | Emits independent high-priority warning flag across UI banners and logs. |

---

## 3. Battery Energy Storage System (BESS) Simulation

To balance intermittent renewable energy and peak demand, a state-of-charge (SoC) model is simulated across every forecast window:

- **Battery Total Capacity:** $500\text{ kWh}$
- **Initial State of Charge:** $80.0\%$ ($400\text{ kWh}$)
- **Safe Operational Boundaries:** $10.0\%$ (floor) to $100.0\%$ (ceiling)
- **Discharge Strategy (Renewable Storage Mode):** The battery absorbs **$30\%$ of total hourly demand**:
  $$\Delta \text{SoC}_{\text{discharge}} = - \frac{0.30 \times \text{Demand (kW)}}{500\text{ kWh}} \times 100\%$$
- **Recharge Strategy (Main Grid Mode):** The battery recharges at **$40\text{ kWh / hour}$** from off-peak grid power:
  $$\Delta \text{SoC}_{\text{charge}} = + \frac{40\text{ kWh}}{500\text{ kWh}} \times 100\% = +8.0\% / \text{hr}$$

---

## 4. Repository Structure

```
├── app.py                  # Catalyst AppSail Flask backend & API routes
├── forecast.py             # Forecast orchestrator: combines predict, switching, and BESS SoC
├── switching.py            # Transition controller logic & unit assertions
├── predict.py              # Inference script for evaluation (QuickML + fallback)
├── prepare.py              # Training data feature preparation
├── train_local.py          # High-availability model training script
├── test_eval.py            # Pre-submission organizer validator (outputs SUCCESS)
├── sample_test_input.csv   # Evaluation sample dataset
├── train_prepared.csv      # Prepared feature dataset for QuickML and training
├── static/
│   └── index.html          # Interactive multi-page dashboard (Overview, Modes, Battery, Log)
├── appsail-python/         # Deployment staging directory for Catalyst AppSail
│   └── app-config.json     # AppSail runtime configuration
└── requirements.txt        # Backend dependencies
```

---

## 5. Local Setup & Execution

### Prerequisites
- Python 3.9+
- Node.js & Zoho Catalyst CLI (`zcatalyst-cli`)

### Installation
```bash
python -m pip install -r requirements.txt
```

### Running Inference Script (`predict.py`)
```bash
python predict.py --input sample_test_input.csv --output predictions.csv
```

### Pre-Submission Self-Test (`test_eval.py`)
```bash
python test_eval.py
```
*Expected Output:*
```text
  HACKSPHERE 3.0 - Pre-Submission Self-Tester    
 Found 'predict.py'.
 Found 'sample_test_input.csv'.
 Successfully imported 'predict(input_df)' function.
Loaded 1000 test rows from 'sample_test_input.csv'.
Your predict.py script is completely valid!
SUCCESS
```

### Running the Web Dashboard Locally
```bash
python app.py
```
Open **`http://localhost:9000/`** in your browser.

---

## 6. Environment Variables (Catalyst QuickML Configuration)

For production deployment or hidden-test execution, configure the following environment variables:

| Variable | Description |
| :--- | :--- |
| `QUICKML_ENDPOINT_URL` | Published QuickML Prediction Endpoint REST URL |
| `QUICKML_ENDPOINT_KEY` | `X-QUICKML-ENDPOINT-KEY` header value |
| `CATALYST_ORG` | Zoho Catalyst Organization ID |
| `ZOHO_CLIENT_ID` | Zoho API OAuth Self-Client ID |
| `ZOHO_CLIENT_SECRET` | Zoho API OAuth Self-Client Secret |
| `ZOHO_REFRESH_TOKEN` | Long-lived OAuth refresh token (scope `QuickML.deployment.READ`) |

*Security Note: Secret keys and tokens should never be committed into public repositories.*
