import json
import time
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List

api_url = "/api/reports"


class ReportAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_scan_report_v2(self, file_format: str, scan_engines: List[str], scan_id: str) -> str:
        """

        Args:
            file_format (str):
            scan_engines (List[str]):
            scan_id (str):

        Returns:
            str
        """
        report_url = f"{api_url}/v2"

        post_data = json.dumps({
            "fileFormat": file_format,
            "reportName": "improved-scan-report",
            "reportFilename": "",
            "sections": [
                "scan-information",
                "results-overview",
                "scan-results",
                "categories",
                "resolved-results",
                "vulnerability-details"
            ],
            "entities": [
                {
                    "entity": "scan",
                    "ids": [scan_id],
                    "tags": []
                }
            ],
            "filters": {
                "scanners": scan_engines,
                "severities": ["high", "medium", "low", "information"],
                "states": ["to-verify", "confirmed", "urgent", "not-exploitable", "proposed-not-exploitable"],
                "status": ["new", "recurrent"]
            },
            "reportType": "ui",
            "emails": []
        })

        response = self.api_client.post_request(relative_url=report_url, data=post_data)
        report_json = response.json()
        report_id = report_json.get("reportId")

        report_status_url = f"/api/reports/{report_id}?returnUrl=true"
        while True:
            response = self.api_client.get_request(relative_url=report_status_url)
            status_json = response.json()
            status = status_json.get("status")

            if status == "completed":
                print("Report has been generated successfully!")
                break
            else:
                print("Generating report, please wait...")
                time.sleep(2)
        return report_id

    def create_scan_report(self, file_format: str, scan_id: str, project_id: str) -> str:
        """

        Args:
            file_format (str):
            scan_id (str):
            project_id (str):

        Returns:
            str
        """
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

        response = self.api_client.post_request(relative_url=report_url, data=post_data)
        report_json = response.json()
        report_id = report_json.get("reportId")

        report_status_url = api_url + f"/{report_id}?returnUrl=true"

        while True:
            response = self.api_client.get_request(relative_url=report_status_url)
            status_json = response.json()
            status = status_json.get("status")

            if status == "completed":
                print("Report has been generated successfully!")
                break
            else:
                print("Generating report, please wait...")
                time.sleep(2)
        return report_id

    def get_scan_report(self, report_id: str) -> dict:
        """

        Args:
            report_id (str):

        Returns:
            dict
        """
        relative_url = api_url + f"/{report_id}/download"

        response = self.api_client.get_request(relative_url=relative_url)
        response_json = json.loads(response.content)
        return response_json

    def get_risk_scan_report(self, scan_id: str, report_type: str) -> dict:
        """

        Args:
            scan_id (str):
            report_type (str):

        Returns:
            dict
        """
        relative_url = f"/api/sca/risk-management/risk-reports/{scan_id}/export?format={report_type}"

        response = self.api_client.get_request(relative_url=relative_url)
        response_json = json.loads(response.content)
        return response_json

    def create_sca_scan_report(self, scan_id: str) -> str:
        """

        Args:
            scan_id (str):

        Returns:
            str
        """
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

        response = self.api_client.post_request(relative_url=report_url, data=data)
        response_json = response.json()
        export_id = response_json['exportId']
        return export_id

    def get_sca_scan_report(self, export_id: str) -> dict:
        """

        Args:
            export_id (str):

        Returns:
            dict
        """
        report_status_url = f"/api/sca/export/requests?exportId={export_id}"
        while True:
            response = self.api_client.get_request(relative_url=report_status_url)
            status_json = response.json()
            status = status_json.get("exportStatus")

            if status == "Completed":
                report_download_url = f"/api/sca/export/requests/{export_id}/download"
                response = self.api_client.get_request(relative_url=report_download_url)
                print("Report has been generated successfully!")
                break
            if status == "Failed":
                print(f"Error: {response.content}")
                break
            else:
                print("Generating report, please wait...")
                time.sleep(2)

        return response.json()


def create_scan_report_v2(file_format: str, scan_engines: List[str], scan_id: str) -> str:
    return ReportAPI().create_scan_report_v2(file_format=file_format, scan_engines=scan_engines, scan_id=scan_id)


def create_scan_report(file_format: str, scan_id: str, project_id: str) -> str:
    return ReportAPI().create_scan_report(file_format=file_format, scan_id=scan_id, project_id=project_id)


def get_scan_report(report_id: str) -> dict:
    return ReportAPI().get_scan_report(report_id=report_id)


def get_risk_scan_report(scan_id: str, report_type: str) -> dict:
    return ReportAPI().get_risk_scan_report(scan_id=scan_id, report_type=report_type)


def create_sca_scan_report(scan_id: str) -> str:
    return ReportAPI().create_sca_scan_report(scan_id=scan_id)


def get_sca_scan_report(export_id: str) -> dict:
    return ReportAPI().get_sca_scan_report(export_id=export_id)
