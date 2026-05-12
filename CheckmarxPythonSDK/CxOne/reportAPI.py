import time
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class ReportAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/reports"
        )

    def create_scan_report_v2(
        self,
        file_format: str,
        scan_engines: List[str],
        scan_id: str,
    ) -> str:
        """
        Args:
            file_format (str):
            scan_engines (List[str]):
            scan_id (str):

        Returns:
            str
        """
        url = f"{self.base_url}/v2"
        payload = {
            "fileFormat": file_format,
            "reportName": "improved-scan-report",
            "reportFilename": "",
            "sections": [
                "scan-information",
                "results-overview",
                "scan-results",
                "categories",
                "resolved-results",
                "vulnerability-details",
            ],
            "entities": [
                {"entity": "scan", "ids": [scan_id], "tags": []}
            ],
            "filters": {
                "scanners": scan_engines,
                "severities": ["high", "medium", "low", "information"],
                "states": [
                    "to-verify",
                    "confirmed",
                    "urgent",
                    "not-exploitable",
                    "proposed-not-exploitable",
                ],
                "status": ["new", "recurrent"],
            },
            "reportType": "ui",
            "emails": [],
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=payload
        )
        report_id = response.json().get("reportId")
        status_url = f"{self.base_url}/{report_id}"
        while True:
            response = self.api_client.call_api(
                method="GET",
                url=status_url,
                params={"returnUrl": "true"},
            )
            status = response.json().get("status")
            if status == "completed":
                print("Report has been generated successfully!")
                break
            else:
                print("Generating report, please wait...")
                time.sleep(2)
        return report_id

    def create_scan_report(
        self, file_format: str, scan_id: str, project_id: str
    ) -> str:
        """
        Args:
            file_format (str):
            scan_id (str):
            project_id (str):

        Returns:
            str
        """
        payload = {
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
                    "ScanResults",
                ],
                "scanners": ["SAST", "SCA", "KICS"],
                "host": "",
            },
        }
        response = self.api_client.call_api(
            method="POST", url=self.base_url, json=payload
        )
        report_id = response.json().get("reportId")
        status_url = f"{self.base_url}/{report_id}"
        while True:
            response = self.api_client.call_api(
                method="GET",
                url=status_url,
                params={"returnUrl": "true"},
            )
            status = response.json().get("status")
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
        url = f"{self.base_url}/{report_id}/download"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_risk_scan_report(
        self, scan_id: str, report_type: str
    ) -> dict:
        """
        Args:
            scan_id (str):
            report_type (str):

        Returns:
            dict
        """
        base = self.api_client.configuration.server_base_url
        url = (
            f"{base}/api/sca/risk-management"
            f"/risk-reports/{scan_id}/export"
        )
        response = self.api_client.call_api(
            method="GET", url=url, params={"format": report_type}
        )
        return response.json()

    def create_sca_scan_report(self, scan_id: str) -> str:
        """
        Args:
            scan_id (str):

        Returns:
            str
        """
        base = self.api_client.configuration.server_base_url
        url = f"{base}/api/sca/export/requests"
        payload = {
            "ScanId": scan_id,
            "FileFormat": "ScanReportJson",
            "ExportParameters": {
                "hideDevAndTestDependencies": False,
                "showOnlyEffectiveLicenses": False,
                "excludePackages": False,
                "excludeLicenses": True,
                "excludeVulnerabilities": False,
                "excludePolicies": True,
            },
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=payload
        )
        return response.json()["exportId"]

    def get_sca_scan_report(self, export_id: str) -> dict:
        """
        Args:
            export_id (str):

        Returns:
            dict
        """
        base = self.api_client.configuration.server_base_url
        status_url = f"{base}/api/sca/export/requests"
        download_url = (
            f"{base}/api/sca/export/requests/{export_id}/download"
        )
        while True:
            response = self.api_client.call_api(
                method="GET",
                url=status_url,
                params={"exportId": export_id},
            )
            status = response.json().get("exportStatus")
            if status == "Completed":
                response = self.api_client.call_api(
                    method="GET", url=download_url
                )
                print("Report has been generated successfully!")
                break
            if status == "Failed":
                print(f"Error: {response.content}")
                break
            else:
                print("Generating report, please wait...")
                time.sleep(2)
        return response.json()


def create_scan_report_v2(
    file_format: str, scan_engines: List[str], scan_id: str
) -> str:
    return ReportAPI().create_scan_report_v2(
        file_format=file_format,
        scan_engines=scan_engines,
        scan_id=scan_id,
    )


def create_scan_report(
    file_format: str, scan_id: str, project_id: str
) -> str:
    return ReportAPI().create_scan_report(
        file_format=file_format, scan_id=scan_id, project_id=project_id
    )


def get_scan_report(report_id: str) -> dict:
    return ReportAPI().get_scan_report(report_id=report_id)


def get_risk_scan_report(scan_id: str, report_type: str) -> dict:
    return ReportAPI().get_risk_scan_report(
        scan_id=scan_id, report_type=report_type
    )


def create_sca_scan_report(scan_id: str) -> str:
    return ReportAPI().create_sca_scan_report(scan_id=scan_id)


def get_sca_scan_report(export_id: str) -> dict:
    return ReportAPI().get_sca_scan_report(export_id=export_id)
