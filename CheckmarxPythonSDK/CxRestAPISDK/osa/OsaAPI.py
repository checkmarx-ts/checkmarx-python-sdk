# encoding: utf-8

import http
import requests
import copy

from pathlib import Path
from requests_toolbelt import MultipartEncoder

from ..auth import AuthenticationAPI
from ..config import CxConfig
from ..exceptions.CxError import BadRequestError, NotFoundError, CxError
from .dto import (
    CxOsaScanDetail, CxOsaState, CxOsaLicense, CxOsaLibrary, CxOsaMatchType,
    CxOsaLocation, CxOsaSeverity, CxOsaVulnerability, CxOsaVulnerabilityState,
    CxOsaVulnerabilityComment, CxOsaSummaryReport
)


class OsaAPI(object):
    """
    osa rest api
    """
    max_try = CxConfig.CxConfig.config.max_try
    base_url = CxConfig.CxConfig.config.url
    verify = CxConfig.CxConfig.config.verify

    def __init__(self):
        self.retry = 0

    def get_all_osa_scan_details_for_project(self, project_id=None, page=None, items_per_page=None):
        """
        Get basic scan details for all CxOSA scans associated with a specified project Id.
        v8.4.2 and up

        Args:
            project_id (int): Unique Id of the project
            page (int, optional): (Number of pages (default 1)
            items_per_page (int, optional): Number of items per page (default 100)

        Returns:
            list: :obj:`list` of :obj:`CxOsaScanDetail`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        osa_scan_details = None

        osa_scans_url = self.base_url + "/osa/scans?projectId=" + str(project_id)

        optionals = []
        if page:
            optionals.append("page=" + str(page))
        if items_per_page:
            optionals.append("items_per_page=" + str(items_per_page))
        if optionals:
            osa_scans_url += "&"
            osa_scans_url += "&".join(optionals)

        headers = copy.deepcopy(AuthenticationAPI.AuthenticationAPI.auth_headers)

        r = requests.get(url=osa_scans_url, headers=headers, verify=OsaAPI.verify)
        if r.status_code == 200:
            a_list = r.json()
            osa_scan_details = [
                CxOsaScanDetail.CxOsaScanDetail(
                    findings_status=item.get("findingsStatus"),
                    scan_detail_id=item.get("id"),
                    start_analyze_time=item.get("startAnalyzeTime"),
                    end_analyze_time=item.get("endAnalyzeTime"),
                    origin=item.get("origin"),
                    source_code_origin=item.get("sourceCodeOrigin"),
                    state=CxOsaState.CxOsaState(
                        state_id=(item.get("state", {}) or {}).get("id"),
                        name=(item.get("state", {}) or {}).get("name"),
                        failure_reason=(item.get("state", {}) or {}).get("failureReason")
                    ),
                    shared_source_location_paths=list(item.get("sharedSourceLocationPaths", "") or "")
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_osa_scan_details_for_project(project_id)
        else:
            raise CxError(r.text, r.status_code)

        return osa_scan_details

    def get_last_osa_scan_id_of_a_project(self, project_id):
        """

        Args:
            project_id (int): Unique Id of the project

        Returns:
            str:  last OSA scan id for project with project_id
        """
        osa_scan_id = None

        all_osa_scan_details = self.get_all_osa_scan_details_for_project(project_id)

        if all_osa_scan_details and len(all_osa_scan_details) > 0:
            osa_scan_id = all_osa_scan_details[0].id

        return osa_scan_id

    def get_osa_scan_by_scan_id(self, scan_id):
        """
        Get CxOSA scan details for the specified CxOSA scan Id.
        v8.4.2 and up

        Args:
            scan_id (str): Unique Id of the OSA scan

        Returns:
           :obj:`CxOsaScanDetail`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        osa_scan_detail = None

        osa_scan_by_scan_id_url = self.base_url + "/osa/scans/{scanId}".format(scanId=scan_id)

        r = requests.get(url=osa_scan_by_scan_id_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
                         verify=OsaAPI.verify)

        if r.status_code == 200:
            a_dict = r.json()
            osa_scan_detail = CxOsaScanDetail.CxOsaScanDetail(
                findings_status=a_dict.get("findingsStatus"),
                scan_detail_id=a_dict.get("id"),
                start_analyze_time=a_dict.get("startAnalyzeTime"),
                end_analyze_time=a_dict.get("endAnalyzeTime"),
                origin=a_dict.get("origin"),
                source_code_origin=a_dict.get("sourceCodeOrigin"),
                state=CxOsaState.CxOsaState(
                    state_id=(a_dict.get("state", {}) or {}).get("id"),
                    name=(a_dict.get("state", {}) or {}).get("name"),
                    failure_reason=(a_dict.get("state", {}) or {}).get("failureReason")
                ),
                shared_source_location_paths=list(a_dict.get("sharedSourceLocationPaths", "") or "")
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_osa_scan_by_scan_id(scan_id)
        else:
            raise CxError(r.text, r.status_code)

        return osa_scan_detail

    def create_an_osa_scan_request(self, project_id, zipped_source_path, origin="REST API"):
        """
        Create a new OSA scan request.
        v8.4.2 and up

        Args:
            project_id (int): The Project Id associated with requested OSA scan
            zipped_source_path (str): the file path of Zipped Open Source code to scan.
            origin (str):The location from which OSA scan was requested. Portal=Default.

        Returns:
            str: the osa scan id

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        scan_id = None

        headers = copy.deepcopy(AuthenticationAPI.AuthenticationAPI.auth_headers)

        file_name = Path(zipped_source_path).name
        m = MultipartEncoder(
            fields={
                "projectId": str(project_id),
                "origin": origin,
                "zippedSource": (file_name, open(zipped_source_path, 'rb'), "application/zip")
            }
        )
        headers.update({"Content-Type": m.content_type})

        osa_scans_url = self.base_url + "/osa/scans" + "?projectId=" + str(project_id)

        r = requests.post(url=osa_scans_url, headers=headers, data=m, verify=OsaAPI.verify)
        if r.status_code == 202:
            scan_id = r.json().get("scanId")
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.create_an_osa_scan_request(project_id, zipped_source_path, origin)
        else:
            raise CxError(r.text, r.status_code)

        return scan_id

    def get_all_osa_file_extensions(self):
        """
        Get all CxOSA file extension information.
        v8.6.0 and up

        Returns:
            str: the osa file extensions, separated by semicolon

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:

        """
        file_extensions = None

        osa_file_extensions_url = self.base_url + "/osa/fileextensions"

        r = requests.get(url=osa_file_extensions_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
                         verify=OsaAPI.verify)
        if r.status_code == 200:
            file_extensions = r.text
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_osa_file_extensions()
        else:
            raise NotFoundError()

        return file_extensions

    def get_osa_licenses_by_id(self, scan_id):
        """
        Get all OSA license details for the specified OSA scan Id.
        v8.6.0 and up

        Args:
            scan_id (str): Unique Id of the OSA scan

        Returns:
            :obj:`list` of :obj:`CxOsaLicense`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        licenses = None

        osa_licenses_url = self.base_url + "/osa/licenses" + "?scanId=" + str(scan_id)

        r = requests.get(
            url=osa_licenses_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=OsaAPI.verify
        )
        if r.status_code == 200:
            a_list = r.json()
            licenses = [
                CxOsaLicense.CxOsaLicense(
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
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_osa_licenses_by_id(scan_id)
        else:
            raise CxError(r.text, r.status_code)

        return licenses

    def get_osa_scan_libraries(self, scan_id, page=None, items_per_page=None):
        """
        Get all the used libraries details for the specified CxOSA scan Id.
        Supported v8.6.0 and up

        Args:
            scan_id (str): Unique Id of the OSA scan
            page (int, optional): (Number of pages (default 1)
            items_per_page (int, optional): Number of items per page (default 100)

        Returns:
            :obj:`list` of :obj:`CxOsaLibrary`

        Raise:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        libraries = None

        osa_libraries_url = self.base_url + "/osa/libraries" + "?scanId=" + str(scan_id)

        optionals = []
        if page:
            optionals.append("page=" + str(page))
        if items_per_page:
            optionals.append("items_per_page=" + str(items_per_page))
        if optionals:
            osa_libraries_url += "&"
            osa_libraries_url += "&".join(optionals)

        r = requests.get(
            url=osa_libraries_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=OsaAPI.verify
        )

        if r.status_code == 200:
            a_list = r.json()
            libraries = [
                CxOsaLibrary.CxOsaLibrary(
                    library_id=item.get("id"),
                    name=item.get("name"),
                    version=item.get("version"),
                    release_date=item.get("releaseDate"),
                    high_unique_vulnerability_count=item.get("highUniqueVulnerabilityCount"),
                    medium_unique_vulnerability_count=item.get("mediumUniqueVulnerabilityCount"),
                    low_unique_vulnerability_count=item.get("lowUniqueVulnerabilityCount"),
                    not_exploitable_vulnerability_count=item.get("notExploitableVulnerabilityCount"),
                    newest_version=item.get("notExploitableVulnerabilityCount"),
                    newest_version_release_date=item.get("newestVersionReleaseDate"),
                    number_of_versions_since_last_update=item.get("numberOfVersionsSinceLastUpdate"),
                    confidence_level=item.get("confidenceLevel"),
                    match_type=CxOsaMatchType.CxOsaMatchType(
                        match_type_id=(item.get("matchType", {}) or {}).get("id"),
                        name=(item.get("matchType", {}) or {}).get("name"),
                        description=(item.get("matchType", {}) or {}).get("description"),
                    ),
                    licenses=item.get("licenses"),
                    outdated=item.get("outdated"),
                    severity=CxOsaSeverity.CxOsaSeverity(
                        severity_id=(item.get("severity", {}) or {}).get("id"),
                        name=(item.get("severity", {}) or {}).get("name")
                    ),
                    risk_score=item.get("riskScore"),
                    locations=[
                        CxOsaLocation.CxOsaLocation(
                            path=location.get("path"),
                            match_type=CxOsaMatchType.CxOsaMatchType(
                                match_type_id=(location.get("matchType", {}) or {}).get("id"),
                                name=(location.get("matchType", {}) or {}).get("name"),
                                description=(location.get("matchType", {}) or {}).get("description")
                            )

                        ) for location in (item.get("locations", []) or [])
                    ],
                    code_usage_status=item.get("codeUsageStatus"),
                    code_reference_count=item.get("codeReferenceCount")
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_osa_scan_libraries(scan_id)
        else:
            raise CxError(r.text, r.status_code)

        return libraries

    def get_osa_scan_vulnerabilities_by_id(self, scan_id, page=None, items_per_page=None, library_id=None,
                                           state_id=None, comment=None, since=None, until=None):
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

        Returns:
            :obj:`list` of :obj:`CxOsaVulnerability`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:

        """
        vulnerabilities = None

        osa_vulnerabilities_url = self.base_url + "/osa/vulnerabilities"

        if scan_id:
            osa_vulnerabilities_url += "?scanId=" + str(scan_id)

            optionals = []
            if page:
                optionals.append("page=" + str(page))
            if items_per_page:
                optionals.append("items_per_page=" + str(items_per_page))
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
                osa_vulnerabilities_url += "&"
                osa_vulnerabilities_url += "&".join(optionals)

        r = requests.get(
            url=osa_vulnerabilities_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=OsaAPI.verify
        )
        if r.status_code == 200:
            a_list = r.json()
            vulnerabilities = [
                CxOsaVulnerability.CxOsaVulnerability(
                    vulnerability_id=item.get("id"),
                    cve_name=item.get("cveName"),
                    score=item.get("score"),
                    severity=CxOsaSeverity.CxOsaSeverity(
                        severity_id=(item.get("severity", {}) or {}).get("id"),
                        name=(item.get("severity", {}) or {}).get("name"),
                    ),
                    publish_date=item.get("publishDate"),
                    url=item.get("url"),
                    description=item.get("description"),
                    recommendations=item.get("recommendations"),
                    source_file_name=item.get("sourceFileName"),
                    library_id=item.get("libraryId"),
                    state=CxOsaVulnerabilityState.CxOsaVulnerabilityState(
                        vulnerability_state_id=(item.get("state", {}) or {}).get("id"),
                        action_type=(item.get("state", {}) or {}).get("actionType"),
                        name=(item.get("state", {}) or {}).get("name")
                    ),
                    comments_amount=item.get("commentsAmount"),
                    similarity_id=item.get("similarityId"),
                    fix_url=item.get("fixUrl")
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_osa_scan_vulnerabilities_by_id(scan_id, library_id, state_id, comment, since, until)
        else:
            raise CxError(r.text, r.status_code)

        return vulnerabilities

    def get_first_vulnerability_id(self, scan_id):
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

    def get_osa_scan_vulnerability_comments_by_id(self, vulnerability_id, project_id):
        """
        Get existing comments for vulnerabilities according to Vulnerability Id and Project Id.
        v9.0 and up


        Args:
            vulnerability_id (str): Unique Id of the vulnerability
            project_id (long): Unique Id of the project

        Returns:
            :obj:`list` of :obj:`CxOsaVulnerabilityComment`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        comment = None

        osa_vulnerability_comment_url = self.base_url + "/osa/vulnerabilities/{vulnerabilityId}/comments".format(
                vulnerabilityId=vulnerability_id
            )

        osa_vulnerability_comment_url += "?projectId=" + str(project_id)

        r = requests.get(
            url=osa_vulnerability_comment_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=OsaAPI.verify
        )

        if r.status_code == 200:
            a_list = r.json()
            comment = [
                CxOsaVulnerabilityComment.CxOsaVulnerabilityComment(
                    user_name=item.get("userName"),
                    time_stamp=item.get("timeStamp"),
                    content=item.get("content")
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_osa_scan_vulnerability_comments_by_id(vulnerability_id, project_id)
        else:
            raise CxError(r.text, r.status_code)

        return comment

    def get_osa_scan_summary_report(self, scan_id):
        """
        Generate a new summary report (.json) for the specified OSA scan Id.
        v8.4.2 and up

        Args:
            scan_id (str): Unique Id of the OSA scan

        Returns:
             :obj:`CxOsaSummaryReport`

        Raises:
            BadRequestError:
            NotFoundError:
            CxError:
        """
        report = None

        osa_reports_url = self.base_url + "/osa/reports" + "?scanId=" + str(scan_id)

        r = requests.get(
            url=osa_reports_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=OsaAPI.verify
        )

        if r.status_code == 200:
            a_dict = r.json()
            report = CxOsaSummaryReport.CxOsaSummaryReport(
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
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_osa_scan_summary_report(scan_id)
        else:
            raise CxError(r.text, r.status_code)

        return report
