# encoding: utf-8
import os
from .httpRequests import get_request, post_request, get_headers
from requests_toolbelt import MultipartEncoder
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED
from .osa.dto import (
    CxOsaScanDetail, CxOsaState, CxOsaLicense, CxOsaLibrary, CxOsaMatchType,
    CxOsaLocation, CxOsaSeverity, CxOsaVulnerability, CxOsaVulnerabilityState,
    CxOsaVulnerabilityComment, CxOsaSummaryReport
)


class OsaAPI(object):
    """
    osa rest api
    """
    @staticmethod
    def get_all_osa_scan_details_for_project(project_id=None, page=1, items_per_page=100, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/scans?projectId={project_id}".format(project_id=project_id)
        optionals = []
        if page:
            optionals.append("page=" + str(page))
        if items_per_page:
            optionals.append("itemsPerPage=" + str(items_per_page))
        if optionals:
            relative_url += "&"
            relative_url += "&".join(optionals)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxOsaScanDetail(
                    findings_status=item.get("findingsStatus"),
                    scan_detail_id=item.get("id"),
                    start_analyze_time=item.get("startAnalyzeTime"),
                    end_analyze_time=item.get("endAnalyzeTime"),
                    origin=item.get("origin"),
                    source_code_origin=item.get("sourceCodeOrigin"),
                    state=CxOsaState(
                        state_id=(item.get("state", {}) or {}).get("id"),
                        name=(item.get("state", {}) or {}).get("name"),
                        failure_reason=(item.get("state", {}) or {}).get("failureReason")
                    ),
                    shared_source_location_paths=list(item.get("sharedSourceLocationPaths", "") or "")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_last_osa_scan_id_of_a_project(project_id, succeeded=True):
        """

        Args:
            project_id (int): Unique Id of the project
            succeeded (bool): True for successful osa scans

        Returns:
            str:  last OSA scan id for project with project_id
        """
        osa_scan_id = None

        if project_id:
            all_osa_scan_details = OsaAPI.get_all_osa_scan_details_for_project(project_id)

            if all_osa_scan_details and len(all_osa_scan_details) > 0:
                if succeeded:
                    all_osa_scan_details = filter(lambda scan: scan.state.name == "Succeeded", all_osa_scan_details)

                all_osa_scan_details = sorted(all_osa_scan_details, key=lambda scan: scan.start_analyze_time,
                                              reverse=True)
                osa_scan_id = all_osa_scan_details[0].id

        return osa_scan_id

    @staticmethod
    def get_osa_scan_by_scan_id(scan_id, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/scans/{scanId}".format(scanId=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxOsaScanDetail(
                findings_status=a_dict.get("findingsStatus"),
                scan_detail_id=a_dict.get("id"),
                start_analyze_time=a_dict.get("startAnalyzeTime"),
                end_analyze_time=a_dict.get("endAnalyzeTime"),
                origin=a_dict.get("origin"),
                source_code_origin=a_dict.get("sourceCodeOrigin"),
                state=CxOsaState(
                    state_id=(a_dict.get("state", {}) or {}).get("id"),
                    name=(a_dict.get("state", {}) or {}).get("name"),
                    failure_reason=(a_dict.get("state", {}) or {}).get("failureReason")
                ),
                shared_source_location_paths=list(a_dict.get("sharedSourceLocationPaths", "") or "")
            )
        return result

    @staticmethod
    def create_an_osa_scan_request(project_id, zipped_source_path, origin="REST API", api_version="1.0"):
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
        m = MultipartEncoder(
            fields={
                "projectId": str(project_id),
                "origin": origin if origin else get_headers().get("cxOrigin"),
                "zippedSource": (file_name, open(zipped_source_path, 'rb'), "application/zip")
            }
        )
        headers = {"Content-Type": m.content_type}
        relative_url = "/cxrestapi/osa/scans" + "?projectId={project_id}".format(project_id=project_id)
        response = post_request(relative_url=relative_url, data=m, headers=get_headers(api_version, headers))
        if response.status_code == ACCEPTED:
            result = response.json().get("scanId")
        return result

    @staticmethod
    def get_all_osa_file_extensions(api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/fileextensions"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.text
        return result

    @staticmethod
    def get_osa_licenses_by_id(scan_id, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/licenses" + "?scanId={scan_id}".format(scan_id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxOsaLicense(
                    license_id=item.get("id"),
                    name=item.get("name"),
                    risk_level=item.get("riskLevel"),
                    copyright_risk_score=item.get("copyrightRiskScore"),
                    patent_risk_score=item.get("patentRiskScore"),
                    copy_left=item.get("copyLeft"),
                    linking=item.get("linking"),
                    royalty_free=item.get("royalityFree"),
                    reference_type=item.get("referenceType"),
                    reference=item.get("reference"),
                    url=item.get("url")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_osa_scan_libraries(scan_id, page=1, items_per_page=100, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/libraries" + "?scanId=" + str(scan_id)
        optionals = []
        if page:
            optionals.append("page=" + str(page))
        if items_per_page:
            optionals.append("itemsPerPage=" + str(items_per_page))
        if optionals:
            relative_url += "&"
            relative_url += "&".join(optionals)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxOsaLibrary(
                    library_id=item.get("id"),
                    name=item.get("name"),
                    version=item.get("version"),
                    release_date=item.get("releaseDate"),
                    high_unique_vulnerability_count=item.get("highUniqueVulnerabilityCount"),
                    medium_unique_vulnerability_count=item.get("mediumUniqueVulnerabilityCount"),
                    low_unique_vulnerability_count=item.get("lowUniqueVulnerabilityCount"),
                    not_exploitable_vulnerability_count=item.get("notExploitableVulnerabilityCount"),
                    newest_version=item.get("newestVersion"),
                    newest_version_release_date=item.get("newestVersionReleaseDate"),
                    number_of_versions_since_last_update=item.get("numberOfVersionsSinceLastUpdate"),
                    confidence_level=item.get("confidenceLevel"),
                    match_type=CxOsaMatchType(
                        match_type_id=(item.get("matchType", {}) or {}).get("id"),
                        name=(item.get("matchType", {}) or {}).get("name"),
                        description=(item.get("matchType", {}) or {}).get("description"),
                    ),
                    licenses=item.get("licenses"),
                    outdated=item.get("outdated"),
                    severity=CxOsaSeverity(
                        severity_id=(item.get("severity", {}) or {}).get("id"),
                        name=(item.get("severity", {}) or {}).get("name")
                    ),
                    risk_score=item.get("riskScore"),
                    locations=[
                        CxOsaLocation(
                            path=location.get("path"),
                            match_type=CxOsaMatchType(
                                match_type_id=(location.get("matchType", {}) or {}).get("id"),
                                name=(location.get("matchType", {}) or {}).get("name"),
                                description=(location.get("matchType", {}) or {}).get("description")
                            )

                        ) for location in (item.get("locations", []) or [])
                    ],
                    code_usage_status=item.get("codeUsageStatus"),
                    code_reference_count=item.get("codeReferenceCount"),
                    package_repository=item.get("packageRepository"),
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_osa_scan_vulnerabilities_by_id(scan_id, page=1, items_per_page=100, library_id=None,
                                           state_id=None, comment=None, since=None, until=None, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/vulnerabilities"
        if scan_id:
            relative_url += "?scanId=" + str(scan_id)
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
                relative_url += "&"
                relative_url += "&".join(optionals)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxOsaVulnerability(
                    vulnerability_id=item.get("id"),
                    cve_name=item.get("cveName"),
                    score=item.get("score"),
                    severity=CxOsaSeverity(
                        severity_id=(item.get("severity", {}) or {}).get("id"),
                        name=(item.get("severity", {}) or {}).get("name"),
                    ),
                    publish_date=item.get("publishDate"),
                    url=item.get("url"),
                    description=item.get("description"),
                    recommendations=item.get("recommendations"),
                    source_file_name=item.get("sourceFileName"),
                    library_id=item.get("libraryId"),
                    state=CxOsaVulnerabilityState(
                        vulnerability_state_id=(item.get("state", {}) or {}).get("id"),
                        action_type=(item.get("state", {}) or {}).get("actionType"),
                        name=(item.get("state", {}) or {}).get("name")
                    ),
                    comments_amount=item.get("commentsAmount"),
                    similarity_id=item.get("similarityId"),
                    fix_url=item.get("fixUrl")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_first_vulnerability_id(scan_id):
        """

        Args:
            scan_id (str): unique id of a osa scan

        Returns:
            str: vulnerability id
        """
        vulnerability_id = None
        vulnerabilities = OsaAPI.get_osa_scan_vulnerabilities_by_id(scan_id)
        if vulnerabilities and len(vulnerabilities):
            vulnerability_id = vulnerabilities[0].id
        return vulnerability_id

    @staticmethod
    def get_osa_scan_vulnerability_comments_by_id(vulnerability_id, project_id, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/vulnerabilities/{vulnerabilityId}/comments?projectId={project_id}".format(
            vulnerabilityId=vulnerability_id,
            project_id=project_id
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxOsaVulnerabilityComment(
                    user_name=item.get("userName"),
                    time_stamp=item.get("timeStamp"),
                    content=item.get("content")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_osa_scan_summary_report(scan_id, api_version="1.0"):
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
        relative_url = "/cxrestapi/osa/reports" + "?scanId=" + str(scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxOsaSummaryReport(
                total_libraries=a_dict.get("totalLibraries"),
                high_vulnerability_libraries=a_dict.get("highVulnerabilityLibraries"),
                medium_vulnerability_libraries=a_dict.get("mediumVulnerabilityLibraries"),
                low_vulnerability_libraries=a_dict.get("lowVulnerabilityLibraries"),
                non_vulnerable_libraries=a_dict.get("nonVulnerableLibraries"),
                vulnerable_and_updated=a_dict.get("vulnerableAndUpdated"),
                vulnerable_and_outdated=a_dict.get("vulnerableAndOutdated"),
                vulnerability_score=a_dict.get("vulnerabilityScore"),
                total_high_vulnerabilities=a_dict.get("totalHighVulnerabilities"),
                total_medium_vulnerabilities=a_dict.get("totalMediumVulnerabilities"),
                total_low_vulnerabilities=a_dict.get("totalLowVulnerabilities")
            )
        return result
