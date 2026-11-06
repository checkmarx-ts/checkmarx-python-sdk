import time
from dataclasses import asdict, is_dataclass
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List, Union
from .dto import (
    ExportParametersSbom,
    ExportParametersScanReport,
    ScaExportFileFormats,
    ScaExportStatus,
)
import logging
logger = logging.getLogger(__name__)

# POST /api/sca/export/requests fileFormat values, grouped by which
# exportParameters shape they expect. RemediatedPackagesJson/
# RemediatedPackages's shape isn't documented by Checkmarx -- callers
# needing specific flags there should pass a plain dict. The full set
# (including RemediatedPackages, undocumented but live-confirmed via
# GET /api/sca/export/file-formats) is cross-checked against that
# endpoint's actual output in get_sca_export_file_formats's test.
SCA_EXPORT_SBOM_FILE_FORMATS = {"CycloneDxJson", "CycloneDxXml", "SpdxJson"}
SCA_EXPORT_SCAN_REPORT_FILE_FORMATS = {
    "ScanReportJson", "ScanReportXml", "ScanReportCsv", "ScanReportPdf",
}
SCA_EXPORT_FILE_FORMATS = (
    SCA_EXPORT_SBOM_FILE_FORMATS
    | SCA_EXPORT_SCAN_REPORT_FILE_FORMATS
    | {"RemediatedPackagesJson", "RemediatedPackages"}
)


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

    def get_sca_export_file_formats(self) -> List[ScaExportFileFormats]:
        """GET /api/sca/export/file-formats -- the fileFormat values
        accepted by each SCA export route (e.g. /requests, the route
        used by create_sca_scan_report).

        Returns:
            List[ScaExportFileFormats]
        """
        base = self.api_client.configuration.server_base_url
        url = f"{base}/api/sca/export/file-formats"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            ScaExportFileFormats.from_dict(item) for item in response.json()
        ]

    def create_sca_scan_report(
        self,
        scan_id: str,
        file_format: str = "ScanReportJson",
        export_parameters: Union[
            ExportParametersSbom, ExportParametersScanReport, dict
        ] = None,
    ) -> str:
        """POST /api/sca/export/requests -- request an SCA export/report
        for a scan. Accepted asynchronously; poll/download the result
        with get_sca_scan_report(export_id).

        Args:
            scan_id (str): The scan to generate a report for.
            file_format (str): One of CycloneDxJson, CycloneDxXml,
                SpdxJson, RemediatedPackagesJson, ScanReportJson,
                ScanReportXml, ScanReportCsv, ScanReportPdf. Default:
                ScanReportJson (matches this method's previous,
                non-parameterized behavior).
            export_parameters: Shape depends on `file_format` --
                ExportParametersSbom for the CycloneDx*/SpdxJson
                formats, ExportParametersScanReport for the
                ScanReport* formats, or a plain dict (e.g. for
                RemediatedPackagesJson, whose exportParameters shape
                Checkmarx does not document). Defaults to the right
                type's defaults for `file_format` if omitted
                (ExportParametersScanReport() when `file_format` is
                any ScanReport* value, matching this method's previous
                hardcoded defaults exactly; ExportParametersSbom()
                for SBOM formats; {} otherwise).

        Returns:
            str: exportId, used to poll/download via
            get_sca_scan_report.
        """
        if file_format not in SCA_EXPORT_FILE_FORMATS:
            raise ValueError(
                f"file_format must be one of {sorted(SCA_EXPORT_FILE_FORMATS)}, "
                f"got {file_format!r}"
            )
        if export_parameters is None:
            if file_format in SCA_EXPORT_SBOM_FILE_FORMATS:
                export_parameters = ExportParametersSbom()
            elif file_format in SCA_EXPORT_SCAN_REPORT_FILE_FORMATS:
                export_parameters = ExportParametersScanReport()
            else:
                export_parameters = {}
        if is_dataclass(export_parameters):
            export_parameters = asdict(export_parameters)

        base = self.api_client.configuration.server_base_url
        url = f"{base}/api/sca/export/requests"
        payload = {
            "ScanId": scan_id,
            "FileFormat": file_format,
            "ExportParameters": export_parameters,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=payload
        )
        return response.json()["exportId"]

    def get_sca_export_status(self, export_id: str) -> ScaExportStatus:
        """GET /api/sca/export/requests?exportId={exportId} -- check
        the status of an SCA export request (and, once Completed, its
        download URL) without blocking/polling. For a one-shot
        poll-until-done-and-download instead, see
        get_sca_scan_report.

        Args:
            export_id (str):

        Returns:
            ScaExportStatus
        """
        base = self.api_client.configuration.server_base_url
        url = f"{base}/api/sca/export/requests"
        response = self.api_client.call_api(
            method="GET", url=url, params={"exportId": export_id},
        )
        return ScaExportStatus.from_dict(response.json())

    def download_sca_export(self, export_id: str) -> Union[dict, bytes]:
        """GET /api/sca/export/requests/{exportId}/download -- download
        a completed SCA export/report. Does not check status first --
        call get_sca_export_status (or wait for "Completed") before
        calling this; downloading one that isn't ready yet may 404.

        Returns dict for JSON export formats (set via
        create_sca_scan_report's file_format), and raw bytes for the
        others (XML/CSV/PDF) -- decided from the response's actual
        Content-Type, not from a remembered file_format.

        Args:
            export_id (str):

        Returns:
            dict: for JSON export formats.
            bytes: for XML/CSV/PDF export formats -- caller is
                responsible for writing to disk / decoding as needed.
        """
        base = self.api_client.configuration.server_base_url
        url = f"{base}/api/sca/export/requests/{export_id}/download"
        response = self.api_client.call_api(method="GET", url=url)
        if "json" in response.headers.get("content-type", "").lower():
            return response.json()
        return response.content

    def get_sca_scan_report(self, export_id: str) -> Union[dict, bytes]:
        """Poll an SCA export request until it completes, then download
        it via download_sca_export.

        Args:
            export_id (str):

        Returns:
            dict: for JSON export formats.
            bytes: for XML/CSV/PDF export formats -- caller is
                responsible for writing to disk / decoding as needed.
        """
        status_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/sca/export/requests"
        )
        while True:
            response = self.api_client.call_api(
                method="GET",
                url=status_url,
                params={"exportId": export_id},
            )
            status = response.json().get("exportStatus")
            if status == "Completed":
                logger.info("Report has been generated successfully!")
                return self.download_sca_export(export_id)
            if status == "Failed":
                logger.error(f"Error: {response.content}")
                return response.json()
            logger.info("Generating report, please wait...")
            time.sleep(2)


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


def get_sca_export_file_formats() -> List[ScaExportFileFormats]:
    return ReportAPI().get_sca_export_file_formats()


def create_sca_scan_report(
    scan_id: str,
    file_format: str = "ScanReportJson",
    export_parameters: Union[
        ExportParametersSbom, ExportParametersScanReport, dict
    ] = None,
) -> str:
    return ReportAPI().create_sca_scan_report(
        scan_id=scan_id,
        file_format=file_format,
        export_parameters=export_parameters,
    )


def get_sca_export_status(export_id: str) -> ScaExportStatus:
    return ReportAPI().get_sca_export_status(export_id=export_id)


def download_sca_export(export_id: str) -> Union[dict, bytes]:
    return ReportAPI().download_sca_export(export_id=export_id)


def get_sca_scan_report(export_id: str) -> Union[dict, bytes]:
    return ReportAPI().get_sca_scan_report(export_id=export_id)
