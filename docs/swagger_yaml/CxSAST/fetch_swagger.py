import json
import urllib.request
import ssl
from pathlib import Path

url = "https://desktop-rmvpboc/cxrestapi/help/swagger/docs/latest"
output_path = Path(__file__).parent / "swagger.json"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with urllib.request.urlopen(url, context=ctx) as response:
    data = json.loads(response.read().decode("utf-8"))
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved {len(data)} top-level keys to {output_path}")
