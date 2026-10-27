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

t = time.time()
try:
    r = requests.post(p.ENDPOINT_URL, json={"data": row}, headers=headers, timeout=180)
    print("status:", r.status_code, "time:", round(time.time() - t, 1), "s")
    print(r.text[:300])
except Exception as e:
    print("failed after", round(time.time() - t, 1), "s:", type(e).__name__)