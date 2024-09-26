import json
from CheckmarxPythonSDK.CxOne.httpRequests import get_request

def get_scan_apisec_risk_overview(scan_id):
    relative_url = f"/api/apisec/static/api/scan/{scan_id}/risks-overview"

    response = get_request(relative_url=relative_url)
    return response.json()
