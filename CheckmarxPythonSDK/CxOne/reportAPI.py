import json
import requests
import time
import os
from CheckmarxPythonSDK.CxOne.httpRequests import get_request, post_request
from CheckmarxPythonSDK.utilities.httpRequests import auth_header
from CheckmarxPythonSDK.CxOne.config import config

api_url = "/api/reports"


def create_scan_report(file_format, scan_id, project_id):
    report_url = api_url

    post_data = json.dumps({
        "fileFormat": file_format,
        "reportType": "ui",
        "reportName": "scan-report",
        "data": {
            "scanId": scan_id,
            "projectId": project_id,
            "branchName": ".unknown",
            "sections": [
                "ScanSummary",
                "ExecutiveSummary",
                "ScanResults"
            ],
            "scanners": [
                "SAST",
                "SCA",
                "KICS"
            ],
            "host": ""
        }
    })

    response = post_request(relative_url=report_url,  data=post_data)
    report_json = response.json()
    report_id = report_json.get("reportId")

    report_status_url = api_url + f"/{report_id}?returnUrl=true"

    while True:
        response = get_request(relative_url=report_status_url)
        status_json = response.json()
        status = status_json.get("status")

        if status == "completed":
            print("Report has been generated successfully!")
            break
        else:
            print("Generating report, please wait...")
            time.sleep(2)
    return report_id


def get_scan_report(report_id):
    relative_url = api_url + f"/{report_id}/download"

    response = get_request(relative_url=relative_url)
    return response.content


def get_risk_scan_report(scan_id, report_type):
    relative_url = f"/api/sca/risk-management/risk-reports/{scan_id}/export?format={report_type}"

    response = get_request(relative_url=relative_url)
    return response.content
