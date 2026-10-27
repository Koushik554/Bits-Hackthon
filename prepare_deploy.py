"""Copies the app into appsail-python/ for `catalyst deploy`.

- Leaves model_local.joblib out: the cloud Python/sklearn may differ, so predict.py retrains
  from train_prepared.csv on first use instead.
- Blanks the hardcoded secrets in the *deployed copy* of predict.py (your root predict.py is untouched).
Run:  python prepare_deploy.py
"""
import json
import os
import re
import shutil

DEST = "appsail-python"
FILES = ["app.py", "forecast.py", "predict.py", "switching.py",
         "sample_test_input.csv", "train_prepared.csv"]
SECRET_PATTERN = re.compile(
    r'(os\.getenv\("(?:QUICKML_ENDPOINT_KEY|ZOHO_CLIENT_ID|ZOHO_CLIENT_SECRET|ZOHO_REFRESH_TOKEN)",\s*)"[^"]*"'
)

for f in FILES:
    shutil.copy(f, os.path.join(DEST, f))

shutil.rmtree(os.path.join(DEST, "static"), ignore_errors=True)
shutil.copytree("static", os.path.join(DEST, "static"))

with open(os.path.join(DEST, "predict.py"), encoding="utf-8") as fh:
    src = fh.read()
src, n = SECRET_PATTERN.subn(r'\1""', src)
with open(os.path.join(DEST, "predict.py"), "w", encoding="utf-8", newline="") as fh:
    fh.write(src)
print(f"Blanked {n} secret defaults in deployed predict.py")

with open(os.path.join(DEST, "requirements.txt"), "w") as fh:
    fh.write("flask\npandas\nnumpy\nrequests\nscikit-learn\njoblib\n")

cfg_path = os.path.join(DEST, "app-config.json")
with open(cfg_path) as fh:
    cfg = json.load(fh)
cfg["command"] = "python3 app.py"
cfg["memory"] = 512
PIP = ("python -m pip install -r ./requirements.txt -t ./ --upgrade "
       "--platform manylinux2014_x86_64 --python-version 3.9 "
       "--implementation cp --only-binary=:all:")
cfg["scripts"] = {"preserve": PIP, "predeploy": PIP}
with open(cfg_path, "w") as fh:
    json.dump(cfg, fh, indent="\t")
print("Deploy folder ready:", DEST)
