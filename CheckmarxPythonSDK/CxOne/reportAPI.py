import time
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
import logging
logger = logging.getLogger(__name__)


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
        severities: List[str] = None,
        states: List[str] = None,
        status: List[str] = None,
        sections: List[str] = None,
        report_type: str = "ui",
        emails: List[str] = None,
        report_filename: str = None,
        timezone: str = None,
    ) -> str:
        """POST /reports/v2 (reportName=improved-scan-report) — generate
        an Improved Scan Report and poll until it's ready.

        Confirmed live: the hardcoded severities filter previously sent
        here -- ["high", "medium", "low", "information"] -- silently
        excludes Critical, the single most severe category. The
        generated report's own reportFilters section confirmed this
        ("excluded": ["Critical"]) against a real scan with Critical
        findings. Fixed by including "critical" in the default.

        Args:
            file_format (str): pdf, json, or csv. Required.
            scan_engines (List[str]): Scanners to include: sast, sca,
                iac, containers, microengines, apisec, byor. Required.
            scan_id (str): The scan to report on. Required.
            severities (List[str], optional): critical, high, medium,
                low, information. Defaults to all five.
            states (List[str], optional): to-verify, not-exploitable,
                proposed-not-exploitable, urgent, confirmed. Defaults
                to all five.
            status (List[str], optional): new, recurrent. Defaults to
                both.
            sections (List[str], optional): scan-information,
                results-overview, scan-results, resolved-results,
                categories, vulnerability-details, scs-vulnerabilities.
                Defaults to every section except scs-vulnerabilities
                (SCS isn't one of this method's scan_engines options).
            report_type (str, optional): cli, ui, or email. Defaults
                to "ui".
            emails (List[str], optional): Recipients; required by the
                API when report_type is "email".
            report_filename (str, optional): Defaults to the server's
                own "Cx_ScanReport_{Scan_Date}" naming when omitted
                (previously this sent an explicit empty string instead
                of omitting the field).
            timezone (str, optional): Applied to "overtime" KPIs.
                Defaults to UTC.

        Returns:
            str: the generated report's id.
        """
        url = f"{self.base_url}/v2"
        payload = {
            "fileFormat": file_format,
            "reportName": "improved-scan-report",
            "sections": sections or [
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
                "severities": severities or [
                    "critical", "high", "medium", "low", "information",
                ],
                "states": states or [
                    "to-verify",
                    "confirmed",
                    "urgent",
                    "not-exploitable",
                    "proposed-not-exploitable",
                ],
                "status": status or ["new", "recurrent"],
            },
            "reportType": report_type,
            "emails": emails or [],
        }
        if report_filename is not None:
            payload["reportFilename"] = report_filename
        if timezone is not None:
            payload["timezone"] = timezone
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
                logger.info("Report has been generated successfully!")
                break
            else:
                logger.info("Generating report, please wait...")
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
                logger.info("Report has been generated successfully!")
                break
            else:
                logger.info("Generating report, please wait...")
                time.sleep(2)
        return report_id

    def get_report_status(self, report_id: str, return_url: bool = True) -> dict:
        """
        Get the status of a report.

        Args:
            report_id (str):
            return_url (bool): Include the download URL in response.
                Default: True

        Returns:
            dict with reportId, status, url, filename
        """
        url = f"{self.base_url}/{report_id}"
        params = {"returnUrl": return_url}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

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
                logger.info("Report has been generated successfully!")
                break
            if status == "Failed":
                logger.error(f"Error: {response.content}")
                break
            else:
                logger.info("Generating report, please wait...")
                time.sleep(2)
        return response.json()


def create_scan_report_v2(
    file_format: str,
    scan_engines: List[str],
    scan_id: str,
    severities: List[str] = None,
    states: List[str] = None,
    status: List[str] = None,
    sections: List[str] = None,
    report_type: str = "ui",
    emails: List[str] = None,
    report_filename: str = None,
    timezone: str = None,
) -> str:
    return ReportAPI().create_scan_report_v2(
        file_format=file_format,
        scan_engines=scan_engines,
        scan_id=scan_id,
        severities=severities,
        states=states,
        status=status,
        sections=sections,
        report_type=report_type,
        emails=emails,
        report_filename=report_filename,
        timezone=timezone,
    )


def create_scan_report(
    file_format: str, scan_id: str, project_id: str
) -> str:
    return ReportAPI().create_scan_report(
        file_format=file_format, scan_id=scan_id, project_id=project_id
    )


def get_report_status(report_id: str, return_url: bool = True) -> dict:
    return ReportAPI().get_report_status(
        report_id=report_id, return_url=return_url
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
