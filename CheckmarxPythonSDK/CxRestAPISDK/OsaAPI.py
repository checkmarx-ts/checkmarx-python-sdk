from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
import os
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED
from .osa.dto import (
    CxOsaScanDetail,
    CxOsaState,
    CxOsaLicense,
    CxOsaLibrary,
    CxOsaMatchType,
    CxOsaLocation,
    CxOsaSeverity,
    CxOsaVulnerability,
    CxOsaVulnerabilityState,
    CxOsaVulnerabilityComment,
    CxOsaSummaryReport,
)


class OsaAPI(object):
    """
    osa rest api
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = api_client.configuration.server_base_url.rstrip("/")

    def get_all_osa_scan_details_for_project(
        self,
        project_id: int = None,
        page: int = 1,
        items_per_page: int = 100,
        api_version: str = "1.0",
    ) -> List[CxOsaScanDetail]:
        """
        Get basic scan details for all CxOSA scans associated with a specified project Id.
        v8.4.2 and up

        Args:
            project_id (int): Unique Id of the project
            page (int, optional): (Number of pages (default 1)
            items_per_page (int, optional): Number of items per page (default 100)
            api_version (str, optional):

        Returns:
            list: :obj:`list` of :obj:`CxOsaScanDetail`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = []
        url = f"{self.base_url}/cxrestapi/osa/scans?projectId={project_id}"
        optionals = []
        if page:
            optionals.append("page=" + str(page))
        if items_per_page:
            optionals.append("itemsPerPage=" + str(items_per_page))
        if optionals:
            url += "&"
            url += "&".join(optionals)
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxOsaScanDetail.from_dict(item) for item in response.json()]
        return result

    def get_last_osa_scan_id_of_a_project(
        self, project_id: int, succeeded: bool = True
    ) -> str:
        """

        Args:
            project_id (int): Unique Id of the project
            succeeded (bool): True for successful osa scans

        Returns:
            str:  last OSA scan id for project with project_id
        """
        osa_scan_id = None

        if project_id:
            all_osa_scan_details = self.get_all_osa_scan_details_for_project(project_id)

            if all_osa_scan_details and len(all_osa_scan_details) > 0:
                if succeeded:
                    all_osa_scan_details = filter(
                        lambda scan: scan.state.name == "Succeeded",
                        all_osa_scan_details,
                    )

                all_osa_scan_details = sorted(
                    all_osa_scan_details,
                    key=lambda scan: scan.start_analyze_time,
                    reverse=True,
                )
                osa_scan_id = all_osa_scan_details[0].id

        return osa_scan_id

    def get_osa_scan_by_scan_id(
        self, scan_id: str, api_version: str = "1.0"
    ) -> CxOsaScanDetail:
        """
        Get CxOSA scan details for the specified CxOSA scan Id.
        v8.4.2 and up

        Args:
            scan_id (str): Unique Id of the OSA scan
            api_version (str, optional):

        Returns:
           :obj:`CxOsaScanDetail`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = None
        url = f"{self.base_url}/cxrestapi/osa/scans/{scan_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxOsaScanDetail.from_dict(response.json())
        return result

    def create_an_osa_scan_request(
        self,
        project_id: int,
        zipped_source_path: str,
        origin: str = "REST API",
        api_version: str = "1.0",
    ) -> str:
        """
        Create a new OSA scan request.
        v8.4.2 and up

        Args:
            project_id (int): The Project Id associated with requested OSA scan
            zipped_source_path (str): the file path of Zipped Open Source code to scan.
            origin (str):The location from which OSA scan was requested. Portal=Default.
            api_version (str, optional):

        Returns:
            str: the osa scan id

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = None
        file_name = os.path.basename(zipped_source_path)
        url = f"{self.base_url}/cxrestapi/osa/scans?projectId={project_id}"
        response = self.api_client.call_api(
            "POST",
            url,
            data={
                "projectId": str(project_id),
                "origin": origin if origin else get_headers().get("cxOrigin"),
            },
            files={
                "zippedSource": (
                    file_name,
                    open(zipped_source_path, "rb"),
                    "application/zip",
                )
            },
            headers=get_headers(api_version),
        )
        if response.status_code == ACCEPTED:
            result = response.json().get("scanId")
        return result

    def get_all_osa_file_extensions(self, api_version: str = "1.0") -> str:
        """
        Get all CxOSA file extension information.
        v8.6.0 and up

        Args:
            api_version (str, optional):

        Returns:
            str: the osa file extensions, separated by semicolon

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:

        """
        result = None
        url = f"{self.base_url}/cxrestapi/osa/fileextensions"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.text
        return result

    def get_osa_licenses_by_id(
        self, scan_id: str, api_version: str = "1.0"
    ) -> List[CxOsaLicense]:
        """
        Get all OSA license details for the specified OSA scan Id.
        v8.6.0 and up

        Args:
            scan_id (str): Unique Id of the OSA scan
            api_version (str, optional):


        Returns:
            :obj:`list` of :obj:`CxOsaLicense`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = None
        url = f"{self.base_url}/cxrestapi/osa/licenses?scanId={scan_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxOsaLicense.from_dict(item) for item in response.json()]
        return result

    def get_osa_scan_libraries(
        self,
        scan_id: str,
        page: int = 1,
        items_per_page: int = 100,
        api_version: str = "1.0",
    ) -> List[CxOsaLibrary]:
        """
        Get all the used libraries details for the specified CxOSA scan Id.
        Supported v8.6.0 and up

        Started from 9.4, api version 3.0, add field "packageRepository"

        Args:
            scan_id (str): Unique Id of the OSA scan
            page (int, optional): (Number of pages (default 1)
            items_per_page (int, optional): Number of items per page (default 100)
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxOsaLibrary`

        Raise:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = []
        url = f"{self.base_url}/cxrestapi/osa/libraries" + "?scanId=" + str(scan_id)
        optionals = []
        if page:
            optionals.append("page=" + str(page))
        if items_per_page:
            optionals.append("itemsPerPage=" + str(items_per_page))
        if optionals:
            url += "&"
            url += "&".join(optionals)
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxOsaLibrary.from_dict(item) for item in response.json()]
        return result

    def get_osa_scan_vulnerabilities_by_id(
        self,
        scan_id: str,
        page: int = 1,
        items_per_page: int = 100,
        library_id: str = None,
        state_id: int = None,
        comment: str = None,
        since: int = None,
        until: int = None,
        api_version: str = "1.0",
    ) -> List[CxOsaVulnerability]:
        """
        Get all the vulnerabilities for the specified CxOSA scan Id.
        v8.4.2 and up

        Args:
            scan_id (str): Unique Id of the OSA scan
            page (int, optional): (Number of pages (default 1)
            items_per_page (int, optional): Number of items per page (default 100)
            library_id (str, optional): Filter by Library Id(s)
            state_id (int, optional):  Filter by State Id(s)
            comment (str, optional): Filter by Comment text
            since (long, optional): Filter by start time (not earlier than timestamp value)
            until (long, optional): Filter by end time (not later than timestamp value)
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxOsaVulnerability`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:

        """
        result = []
        url = f"{self.base_url}/cxrestapi/osa/vulnerabilities"
        if scan_id:
            url += "?scanId=" + str(scan_id)
            optionals = []
            if page:
                optionals.append("page=" + str(page))
            if items_per_page:
                optionals.append("itemsPerPage=" + str(items_per_page))
            if library_id:
                optionals.append("libraryId=" + library_id)
            if state_id:
                optionals.append("stateId=" + str(state_id))
            if comment:
                optionals.append("comment=" + comment)
            if since:
                optionals.append("since=" + str(since))
            if until:
                optionals.append("until=" + str(until))
            if optionals:
                url += "&"
                url += "&".join(optionals)
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxOsaVulnerability.from_dict(item) for item in response.json()]
        return result

    def get_first_vulnerability_id(self, scan_id: str) -> str:
        """

        Args:
            scan_id (str): unique id of a osa scan

        Returns:
            str: vulnerability id
        """
        vulnerability_id = None
        vulnerabilities = self.get_osa_scan_vulnerabilities_by_id(scan_id)
        if vulnerabilities and len(vulnerabilities):
            vulnerability_id = vulnerabilities[0].id
        return vulnerability_id

    def get_osa_scan_vulnerability_comments_by_id(
        self, vulnerability_id: str, project_id: int, api_version: str = "1.0"
    ) -> List[CxOsaVulnerabilityComment]:
        """
        Get existing comments for vulnerabilities according to Vulnerability Id and Project Id.
        v9.0 and up


        Args:
            vulnerability_id (str): Unique Id of the vulnerability
            project_id (long): Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxOsaVulnerabilityComment`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = []
        url = f"{self.base_url}/cxrestapi/osa/vulnerabilities/{vulnerability_id}/comments?projectId={project_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [
                CxOsaVulnerabilityComment.from_dict(item) for item in response.json()
            ]
        return result

    def get_osa_scan_summary_report(
        self, scan_id: str, api_version: str = "1.0"
    ) -> CxOsaSummaryReport:
        """
        Generate a new summary report (.json) for the specified OSA scan Id.
        v8.4.2 and up

        Args:
            scan_id (str): Unique Id of the OSA scan
            api_version (str, optional):

        Returns:
             :obj:`CxOsaSummaryReport`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        result = None
        url = f"{self.base_url}/cxrestapi/osa/reports" + "?scanId=" + str(scan_id)
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxOsaSummaryReport.from_dict(response.json())
        return result
