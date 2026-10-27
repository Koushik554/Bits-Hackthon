import time
import requests
import predict as p

headers = {
    "X-QUICKML-ENDPOINT-KEY": p.ENDPOINT_KEY,
    "Authorization": f"Zoho-oauthtoken {p.get_access_token()}",
    "CATALYST-ORG": p.CATALYST_ORG,
    "Environment": "Development",
    "Content-Type": "application/json",
}
row = {"hour": 17, "dayofweek": 0, "ambient_temp_c": 30.5,
       "humidity_pct": 62.21, "solar_irradiance_wm2": 40}


def call(payload, label):
    t = time.time()
    try:
        r = requests.post(p.ENDPOINT_URL, json=payload, headers=headers, timeout=25)
        print(label, "| status", r.status_code, "|", round(time.time() - t, 1), "s |", r.text[:120])
    except Exception as e:
        print(label, "| FAILED after", round(time.time() - t, 1), "s |", type(e).__name__)


print("--- A: 10 requests, one at a time ---")
for i in range(10):
    call({"data": row}, f"seq {i+1}")

print("--- B: one request with a list of 5 rows ---")
call({"data": [row] * 5}, "batch5")

print("--- C: one request with a list of 50 rows ---")
call({"data": [row] * 50}, "batch50")