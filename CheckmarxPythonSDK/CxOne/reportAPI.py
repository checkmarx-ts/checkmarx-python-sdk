import json
import time
from CheckmarxPythonSDK.CxOne.httpRequests import get_request, post_request

api_url = "/api/reports"

def create_scan_report_v2(file_format, scan_engines, scan_id):
    report_url = f"{api_url}/v2"

    post_data = json.dumps({
        "fileFormat": file_format,
        "reportType": "ui",
        "reportName": "improved-scan-report",
        "reportFilename": "",
        "sections":[
            "scan-information",
            "results-overview",
            "scan-results",
            "categories",
            "resolved-results",
            "vulnerability-details"
            ],
        "entities":[
            {
                "entity":"scan",
                "ids":[scan_id],
                "tags":[]
                }
            ],
        "filters":{
            "scanners":scan_engines,
            "severities":["high","medium","low","information"],
            "states":["to-verify","confirmed","urgent","not-exploitable","proposed-not-exploitable"],
            "status":["new","recurrent"]
            },
        "reportType":"ui",
        "emails":[]
    })
    
    response = post_request(relative_url=report_url, data=post_data)
    report_json = response.json()
    report_id = report_json.get("reportId")

    report_status_url = f"/api/reports/{report_id}?returnUrl=true"
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
    response_json = json.loads(response.content)
    return response_json


def get_risk_scan_report(scan_id, report_type):
    relative_url = f"/api/sca/risk-management/risk-reports/{scan_id}/export?format={report_type}"

    response = get_request(relative_url=relative_url)
    response_json = json.loads(response.content)
    return response_json

def create_sca_scan_report(scan_id):
    report_url = f"/api/sca/export/requests"

    data = json.dumps({
        "ScanId": scan_id,
        "FileFormat": "ScanReportJson",
        "ExportParameters": {
            "hideDevAndTestDependencies": False,
            "showOnlyEffectiveLicenses": False,
            "excludePackages": False,
            "excludeLicenses": True,
            "excludeVulnerabilities": False,
            "excludePolicies": True
        }
    })

    response = post_request(relative_url=report_url, data=(data))
    response_json = response.json()
    export_id = response_json['exportId']
    return export_id

def get_sca_scan_report(export_id):
    report_status_url = f"/api/sca/export/requests?exportId={export_id}"
    while True:
        response = get_request(relative_url=report_status_url)
        status_json = response.json()
        status = status_json.get("exportStatus")

        if status == "Completed":
            report_download_url = f"/api/sca/export/requests/{export_id}/download"
            response = get_request(relative_url=report_download_url)
            print("Report has been generated successfully!")
            break
        if status == "Failed":
            print(f"Error: {response.content}")
            break
        else:
            print("Generating report, please wait...")
            time.sleep(2)
    
    return response.json()