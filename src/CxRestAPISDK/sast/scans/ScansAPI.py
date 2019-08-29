# encoding: utf-8

import requests
import http
import json

from ...config import CxConfig
from ...auth import AuthenticationAPI
from ...exceptions.CxError import BadRequestError, NotFoundError, UnknownHttpStatusError
from ...sast.projects.dto import CxLink, CxProject
from ...sast.projects.dto.presets import CxPreset
from ...sast.engines.dto import CxEngineServer, CxEngineConfiguration
from .dto import CxSchedulingSettings, CxScanState, CxPolicyFindingsStatus, \
    CxResultsStatistics, CxPolicyFindingResponse, CxStatus, CxFinishedScanStatus, CxStatisticsResult, \
    CxCreateNewScanResponse, CxCreateScan, CxRegisterScanReportResponse, CxScanType, CxScanDetail, CxScanReportStatus, \
    CxDateAndTime, CxScanQueueDetail, CxScanStage, CxLanguageState, CxStatusDetail
from .dto.scanSettings import CxScanSettings, CxCreateScanSettingsResponse,  \
    CxEmailNotification, CxCreateScanSettingsRequestBody, CxLanguage


class ScansAPI(object):
    """
    scans API
    """
    max_try = CxConfig.CxConfig.config.max_try
    base_url = CxConfig.CxConfig.config.url
    all_scans_url = base_url + "/sast/scans"
    sast_scan_url = base_url + "/sast/scans/{id}"
    statistics_results_url = base_url + "/sast/scans/{id}/resultsStatistics"
    scans_queue_url = base_url + "/sast/scansQueue/{id}"
    all_scan_queue_url = base_url + "/sast/scansQueue"
    scan_settings_url = base_url + "/sast/scanSettings/{projectId}"
    all_scan_settings_url = base_url + "/sast/scanSettings"
    schedule_settings_url = base_url + "/sast/project/{projectId}/scheduling"
    scan_results_ticket_url = base_url + "/sast/results/tickets"
    policy_findings_url = base_url + "/sast/projects/{id}/publisher/policyFindings"
    policy_findings_status_url = base_url + "/sast/projects/{id}/publisher/policyFindings/status"
    register_scan_report_url = base_url + "/reports/sastScan"
    report_status_url = base_url + "/reports/sastScan/{id}/status"
    report_url = base_url + "/reports/sastScan/{id}"

    def __init__(self):
        self.retry = 0

    @staticmethod
    def __construct_scan(item):
        """
        construct scan object

        Args:
            item （dict):

        Returns:
            :obj:`CxScanDetail`
        """
        return CxScanDetail.CxScanDetail(
            scan_id=item.get("id"),
            project=CxProject.CxProject(
                project_id=item.get("project", {}).get("id"),
                name=item.get("project", {}).get("name"),
                link=item.get("project", {}).get("link")
            ),
            status=CxStatus.CxStatus(
                status_id=item.get("status", {}).get("id"),
                name=item.get("status", {}).get("name"),
                details=CxStatusDetail.CxStatusDetail(
                    stage=item.get("status", {}).get("details", {}).get("stage"),
                    step=item.get("status", {}).get("details", {}).get("step")
                )
            ),
            scan_type=CxScanType.CxScanType(
                scan_type_id=item.get("scanType", {}).get("id"),
                value=item.get("scanType", {}).get("value")
            ),
            comment=item.get("comment"),
            date_and_time=CxDateAndTime.CxDateAndTime(
                started_on=(item.get("dateAndTime", {}) or {}).get("startedOn"),
                finished_on=(item.get("dateAndTime", {}) or {}).get("finishedOn"),
                engine_started_on=(item.get("dateAndTime", {}) or {}).get("engineStartedOn"),
                engine_finished_on=(item.get("dateAndTime", {}) or {}).get("engineFinishedOn")
            ),
            results_statistics=CxResultsStatistics.CxResultsStatistics(
                link=(item.get("resultsStatistics", {}) or {}).get("link")
            ),
            scan_state=CxScanState.CxScanState(
                path=(item.get("scanState", {}) or {}).get("path"),
                source_id=(item.get("scanState", {}) or {}).get("sourceId"),
                files_count=(item.get("scanState", {}) or {}).get("filesCount"),
                lines_of_code=(item.get("scanState", {}) or {}).get("linesOfCode"),
                failed_lines_of_code=(item.get("scanState", {}) or {}).get("failedLinesOfCode"),
                cx_version=(item.get("scanState", {}) or {}).get("cxVersion"),
                language_state_collection=[
                    CxLanguageState.CxLanguageState(
                        language_id=language_state.get("languageID"),
                        language_name=language_state.get("languageName"),
                        language_hash=language_state.get("languageHash"),
                        state_creation_date=language_state.get("stateCreationDate")
                    ) for language_state in ((item.get("scanState", {}) or {}).get("languageStateCollection", {}) or {})
                ]
            ),
            owner=item.get("owner"),
            origin=item.get("origin"),
            initiator_name=item.get("initiatorName"),
            owning_team_id=item.get("owningTeamId"),
            is_public=item.get("isPublic"),
            is_locked=item.get("isLocked"),
            is_incremental=item.get("isIncremental"),
            scan_risk=item.get("scanRisk"),
            scan_risk_severity=item.get("scanRiskSeverity"),
            engine_server=CxEngineServer.CxEngineServer(
                engine_server_id=(item.get("engineServer", {}) or {}).get("id"),
                name=(item.get("engineServer", {}) or {}).get("name"),
                link=(item.get("engineServer", {}) or {}).get("link"),
            ),
            finished_scan_status=CxFinishedScanStatus.CxFinishedScanStatus(
                scan_status_id=(item.get("finishedScanStatus", {}) or {}).get("id"),
                value=(item.get("finishedScanStatus", {}) or {}).get("value")
            ),
            partial_scan_reasons=item.get("partialScanReasons")
        )

    def get_all_scans_for_project(self, project_id=None, scan_status=None, last=None):
        """
        Get details of all SAST scans for a specific project.


        Args:
            project_id (int):
            scan_status (str): possible values are 1="New", 2="PreScan", 3="Queued", 4="Scanning", 6="PostScan",
                                7="Finished", 8="Canceled", 9="Failed", 10="SourcePullingAndDeployment", 1001="None"
            last (int): number of last scans
        Returns:
            :obj:`list` of :obj:`CxScanDetail`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError

        """
        all_scans = []

        if project_id:
            if "?" not in self.all_scans_url:
                self.all_scans_url += "?"
            self.all_scans_url += "projectId={}".format(project_id)
        if scan_status:
            if "?" not in self.all_scans_url:
                self.all_scans_url += "?"
            self.all_scans_url += "scanStatus={}".format(scan_status)
        if last:
            if "?" not in self.all_scans_url:
                self.all_scans_url += "?"
            self.all_scans_url += "last={}".format(last)

        r = requests.get(self.all_scans_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            a_list = r.json()
            all_scans = [
                self.__construct_scan(item) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_scans_for_project(project_id, scan_status, last)
        else:
            raise UnknownHttpStatusError()

        return all_scans

    def get_last_scan_id_of_a_project(self, project_id):
        """
        get the last scan id of a project

        Args:
            project_id (int):

        Returns:
            int: scan id
        """
        scan_id = None

        if project_id:
            all_scans_for_this_project = self.get_all_scans_for_project(project_id)
            if len(all_scans_for_this_project) > 0:
                scan_id = all_scans_for_this_project[0].id

        return scan_id

    def create_new_scan(self, project_id, is_incremental=False, is_public=True, force_scan=True, comment=""):
        """
        Create a new SAST scan and assign it to a project.

        Args:
            project_id (int):
            is_incremental (bool):
            is_public (bool):
            force_scan (bool):
            comment (str):

        Returns:
            :obj:`CxCreateNewScanResponse`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        scan = None

        post_body = CxCreateScan.CxCreateScan(
            project_id, is_incremental, is_public, force_scan, comment
        ).get_post_data()

        r = requests.post(url=self.all_scans_url, data=post_body,
                          headers=AuthenticationAPI.AuthenticationAPI.auth_headers)

        if r.status_code == 201:
            a_dict = r.json()
            scan = CxCreateNewScanResponse.CxCreateNewScanResponse(
                scan_id=a_dict.get("id"),
                link=CxLink.CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.create_new_scan(project_id, is_incremental, is_public, force_scan, comment)
        else:
            raise UnknownHttpStatusError()

        return scan

    def get_sast_scan_details_by_scan_id(self, scan_id):
        """
        Get details of a specific SAST scan.

        Args:
            scan_id (int):

        Returns:
            :obj:`CxScanDetail`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        scan_detail = None

        self.sast_scan_url = self.sast_scan_url.format(id=scan_id)

        r = requests.get(self.sast_scan_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            item = r.json()
            scan_detail = self.__construct_scan(item)
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_sast_scan_details_by_scan_id(scan_id)
        else:
            raise UnknownHttpStatusError()

        return scan_detail

    def add_or_update_a_comment_by_scan_id(self, scan_id, comment):
        """
        Add a new comment or update an existing comment according to the scan Id.

        Args:
            scan_id (int):
            comment (str):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        is_successful = False

        self.sast_scan_url = self.sast_scan_url.format(id=scan_id)
        patch_data = json.dumps(
            {
                "comment": comment
            }
        )
        r = requests.patch(url=self.sast_scan_url, data=patch_data,
                           headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 204:
            is_successful = True
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.add_or_update_a_comment_by_scan_id(scan_id, comment)
        else:
            raise UnknownHttpStatusError()

        return is_successful

    def delete_scan_by_scan_id(self, scan_id):
        """
        Delete specific SAST scan according to scan Id.

        Args:
            scan_id (int):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        is_successful = False
        self.sast_scan_url = self.sast_scan_url.format(id=scan_id)
        r = requests.delete(url=self.sast_scan_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 202:
            is_successful = True
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.delete_scan_by_scan_id(scan_id)
        else:
            raise UnknownHttpStatusError()

        return is_successful

    def get_statistics_results_by_scan_id(self, scan_id):
        """
        Get statistic results for a specific scan.

        Args:
            scan_id (int):

        Returns:
            :obj:`CxStatisticsResult`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        statistics = None

        self.statistics_results_url = self.statistics_results_url.format(id=scan_id)
        r = requests.get(url=self.statistics_results_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            item = r.json()
            statistics = CxStatisticsResult.CxStatisticsResult(
                high_severity=item.get("highSeverity"),
                medium_severity=item.get("mediumSeverity"),
                low_severity=item.get("lowSeverity"),
                info_severity=item.get("infoSeverity"),
                statistics_calculation_date=item.get("statisticsCalculationDate")
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_statistics_results_by_scan_id(scan_id)
        else:
            raise UnknownHttpStatusError()

        return statistics

    @staticmethod
    def __construct_scan_queue_detail(item):
        return CxScanQueueDetail.CxScanQueueDetail(
            scan_queue_detail_id=item.get("id"),
            stage=CxScanStage.CxScanStage(
                scan_stage_id=(item.get("stage", {}) or {}).get("id"),
                value=(item.get("stage", {}) or {}).get("value")
            ),
            stage_details=item.get("stageDetails"),
            step_details=item.get("stepDetails"),
            project=CxProject.CxProject(
                project_id=(item.get("project", {}) or {}).get("id"),
                name=(item.get("project", {}) or {}).get("name"),
                link=CxLink.CxLink(
                    rel=((item.get("project", {}) or {}).get("link", {}) or {}).get("rel"),
                    uri=((item.get("project", {}) or {}).get("link", {}) or {}).get("uri")
                )
            ),
            engine=CxEngineServer.CxEngineServer(
                engine_server_id=(item.get("engine", {}) or {}).get("id"),
                link=CxLink.CxLink(
                    rel=((item.get("engine", {}) or {}).get("link", {}) or {}).get("rel"),
                    uri=((item.get("engine", {}) or {}).get("link", {}) or {}).get("uri")
                )
            ),
            languages=[
                CxLanguage.CxLanguage(
                    language_id=language.get("id"),
                    name=language.get("name")
                ) for language in (item.get("languages", []) or [])
            ],
            team_id=item.get("teamId"),
            date_created=item.get("dateCreated"),
            queued_on=item.get("queuedOn"),
            engine_started_on=item.get("engineStaredOn"),
            completed_on=item.get("completedOn"),
            loc=item.get("loc"),
            is_incremental=item.get("isIncremental"),
            is_public=item.get("isPublic"),
            origin=item.get("origin"),
            queue_position=item.get("queuePosition"),
            total_percent=item.get("totalPercent"),
            stage_percent=item.get("stagePercent"),
            initiator=item.get("initiator")
        )

    def get_scan_queue_details_by_scan_id(self, scan_id):
        """
        Get details of a specific CxSAST scan in the scan queue according to the scan Id.

        Args:
            scan_id (int):

        Returns:
            :obj:`CxScanQueueDetail`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        scan_queue_details = None

        self.scans_queue_url = self.scans_queue_url.format(id=scan_id)
        r = requests.get(url=self.scans_queue_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            item = r.json()
            scan_queue_details = self.__construct_scan_queue_detail(item)
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_scan_queue_details_by_scan_id(scan_id)
        else:
            raise UnknownHttpStatusError()

        return scan_queue_details

    def update_queued_scan_status_by_scan_id(self, scan_id, status_id, status_value):
        """
        Update (Cancel) a running scan in the queue according to the scan Id.


        Args:
            scan_id (int):
            status_id (int):
            status_value (str):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        is_successful = False
        self.scans_queue_url = self.scans_queue_url.format(id=scan_id)

        patch_data = json.dumps(
            {
                "status": {
                    "id": status_id,
                    "value": status_value
                }
            }
        )

        r = requests.patch(url=self.scans_queue_url, data=patch_data,
                           headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            is_successful = True
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.update_queued_scan_status_by_scan_id(scan_id, status_id, status_value)
        else:
            raise UnknownHttpStatusError()

        return is_successful

    def get_all_scan_details_in_queue(self, project_id=None):
        """
        Get details of all SAST scans in the scans queue.
        :return:

        Args:
            project_id （int):

        Returns:
            :obj:`list` of :obj:`CxScanQueueDetail`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """

        all_scan_details_in_queue = None

        if project_id:
            self.all_scan_queue_url = self.all_scan_queue_url + "?projectId=" + str(project_id)

        r = requests.get(url=self.all_scan_queue_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            a_list = r.json()
            all_scan_details_in_queue = [self.__construct_scan_queue_detail(item) for item in a_list]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_scan_details_in_queue(project_id)
        else:
            raise UnknownHttpStatusError()

        return all_scan_details_in_queue

    def get_scan_settings_by_project_id(self, project_id):
        """
        Get scan settings by project Id.

        Args:
            project_id (int):

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        scan_settings = None
        self.scan_settings_url = self.scan_settings_url.format(projectId=project_id)

        r = requests.get(url=self.scan_settings_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            a_dict = r.json()
            scan_settings = CxScanSettings.CxScanSettings(
                project=CxProject.CxProject(
                    project_id=(a_dict.get("project", {}) or {}).get("id"),
                    link=CxLink.CxLink(
                        rel=(a_dict.get("project", {}) or {}).get("link", {}).get("rel"),
                        uri=(a_dict.get("project", {}) or {}).get("link", {}).get("uri")
                    )
                ),
                preset=CxPreset.CxPreset(
                    preset_id=(a_dict.get("preset", {}) or {}).get("id"),
                    link=CxLink.CxLink(
                        rel=(a_dict.get("preset", {}) or {}).get("link", {}).get("rel"),
                        uri=(a_dict.get("preset", {}) or {}).get("link", {}).get("uri")
                    )
                ),
                engine_configuration=CxEngineConfiguration.CxEngineConfiguration(
                    engine_configuration_id=(a_dict.get("engineConfiguration", {}) or {}).get("id"),
                    link=CxLink.CxLink(
                        rel=(a_dict.get("engineConfiguration", {}) or {}).get("link", {}).get("rel"),
                        uri=(a_dict.get("engineConfiguration", {}) or {}).get("link", {}).get("uri")
                    )
                ),
                post_scan_action=a_dict.get("postScanAction"),
                email_notifications=CxEmailNotification.CxEmailNotification(
                    failed_scan=(a_dict.get("emailNotifications", {}) or {}).get("failedScan"),
                    before_scan=(a_dict.get("emailNotifications", {}) or {}).get("beforeScan"),
                    after_scan=(a_dict.get("emailNotifications", {}) or {}).get("afterScan"),
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_scan_settings_by_project_id(project_id)
        else:
            raise UnknownHttpStatusError()

        return scan_settings

    def define_sast_scan_settings(self, project_id, preset_id=1, engine_configuration_id=1, post_scan_action_id=None,
                                  failed_scan_emails=None, before_scan_emails=None, after_scan_emails=None):
        """
        Define the SAST scan settings according to a project (preset and engine configuration).

        Args:
            project_id (int):
            preset_id (int):
            engine_configuration_id (int):
            post_scan_action_id (int):
            failed_scan_emails (:obj:`list` of :obj:`str`):
            before_scan_emails (:obj:`list` of :obj:`str`):
            after_scan_emails (:obj:`list` of :obj:`str`):

        Returns:
            :obj:`CxCreateScanSettingsResponse`

        Raises：
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        sast_scan_settings = None

        post_body_data = CxCreateScanSettingsRequestBody.CxCreateScanSettingsRequestBody(
            project_id=project_id,
            preset_id=preset_id,
            engine_configuration_id=engine_configuration_id,
            post_scan_action_id=post_scan_action_id,
            failed_scan_emails=failed_scan_emails,
            before_scan_emails=before_scan_emails,
            after_scan_emails=after_scan_emails
        ).get_post_data()
        r = requests.post(url=self.all_scan_settings_url, data=post_body_data,
                          headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            a_dict = r.json()
            sast_scan_settings = CxCreateScanSettingsResponse.CxCreateScanSettingsResponse(
                scan_setting_response_id=a_dict.get("id"),
                link=CxLink.CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.define_sast_scan_settings(project_id, preset_id, engine_configuration_id, post_scan_action_id,
                                           failed_scan_emails, before_scan_emails, after_scan_emails)
        else:
            raise UnknownHttpStatusError()

        return sast_scan_settings

    def update_sast_scan_settings(self, project_id, preset_id=1, engine_configuration_id=1, post_scan_action_id=None,
                                  failed_scan_emails=None, before_scan_emails=None, after_scan_emails=None):
        """
        Update the SAST scan settings for a project
        (preset, engine configuration, custom actions and email notifications).

        Args:
            project_id (int):
            preset_id (int):
            engine_configuration_id (int):
            post_scan_action_id (int):
            failed_scan_emails (:obj:`list` of :obj:`str`):
            before_scan_emails (:obj:`list` of :obj:`str`):
            after_scan_emails (:obj:`list` of :obj:`str`):

        Returns:
            :obj:`CxCreateScanSettingsResponse`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        sast_scan_settings = None

        post_body_data = CxCreateScanSettingsRequestBody.CxCreateScanSettingsRequestBody(
            project_id=project_id,
            preset_id=preset_id,
            engine_configuration_id=engine_configuration_id,
            post_scan_action_id=post_scan_action_id,
            failed_scan_emails=failed_scan_emails,
            before_scan_emails=before_scan_emails,
            after_scan_emails=after_scan_emails
        ).get_post_data()
        r = requests.put(url=self.all_scan_settings_url, data=post_body_data,
                         headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            a_dict = r.json()
            sast_scan_settings = CxCreateScanSettingsResponse.CxCreateScanSettingsResponse(
                scan_setting_response_id=a_dict.get("id"),
                link=CxLink.CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.update_sast_scan_settings(project_id, preset_id, engine_configuration_id, post_scan_action_id,
                                           failed_scan_emails, before_scan_emails, after_scan_emails)
        else:
            raise UnknownHttpStatusError()

        return sast_scan_settings

    def define_sast_scan_scheduling_settings(self, project_id, schedule_type, schedule_days, schedule_time):
        """
        Define SAST scan scheduling settings for a project.


        Args:
            project_id (int):
            schedule_type (str):
            schedule_days (:obj:`list` of :obj:`str`):
            schedule_time (str):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        is_successful = False
        self.schedule_settings_url = self.schedule_settings_url.format(projectId=project_id)

        post_body_data = CxSchedulingSettings.CxSchedulingSettings(
            schedule_type=schedule_type,
            schedule_days=schedule_days,
            schedule_time=schedule_time
        ).get_post_data()

        r = requests.put(url=self.schedule_settings_url, data=post_body_data,
                         headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 204:
            is_successful = True
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.define_sast_scan_scheduling_settings(project_id, schedule_type, schedule_days, schedule_time)
        else:
            raise UnknownHttpStatusError()

        return is_successful

    def assign_ticket_to_scan_results(self, results_id, ticket_id):
        """
        Assign ticket to scan results according to scan results and ticket Id.

        Args:
            results_id (str):
            ticket_id (str):

        Returns:
            bool

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        is_successful = False
        post_body_data = json.dumps(
            {
                "resultsId": list(results_id),
                "ticketId": ticket_id
            }
        )

        r = requests.post(url=self.scan_results_ticket_url, data=post_body_data,
                          headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            is_successful = True
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.assign_ticket_to_scan_results(results_id, ticket_id)
        else:
            raise UnknownHttpStatusError()

        return is_successful

    def publish_last_scan_results_to_management_and_orchestration_by_project_id(self, project_id):
        """
        Publish last scan results to Management and Orchestration for a specific project
        (only for policy management evaluation in v8.9.0).

        Args:
            project_id (int):

        Returns:
            :obj:`CxPolicyFindingResponse`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        policy_finding_response = None

        self.policy_findings_url = self.policy_findings_url.format(id=project_id)
        r = requests.post(url=self.policy_findings_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 201:
            a_dict = r.json()
            policy_finding_response = CxPolicyFindingResponse.CxPolicyFindingResponse(
                policy_finding_id=a_dict.get("id"),
                link=CxLink.CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.publish_last_scan_results_to_management_and_orchestration_by_project_id(project_id)
        else:
            raise UnknownHttpStatusError()

        return policy_finding_response

    def get_the_publish_last_scan_results_to_management_and_orchestration_status(self, project_id):
        """
        Get the status of publish last scan results to Management and Orchestration layer for a specific project.
        :param project_id:
        :return:

        Args:
            project_id (int):

        Returns:
            :obj:`CxPolicyFindingsStatus`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError

        """
        policy_finding_status = None

        self.policy_findings_status_url = self.policy_findings_status_url.format(id=project_id)
        r = requests.get(url=self.policy_findings_status_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)

        if r.status_code == 200:
            a_dict = r.json()
            policy_finding_status = CxPolicyFindingsStatus.CxPolicyFindingsStatus(
                project=CxProject.CxProject(
                    project_id=(a_dict.get("project", {}) or {}).get("id"),
                    link=CxLink.CxLink(
                        rel=((a_dict.get("project", {}) or {}).get("link", {}) or {}).get("rel"),
                        uri=((a_dict.get("project", {}) or {}).get("link", {}) or {}).get("uri")
                    )
                ),
                scan=CxCreateNewScanResponse.CxCreateNewScanResponse(
                    scan_id=(a_dict.get("scan", {}) or {}).get("id"),
                    link=CxLink.CxLink(
                        rel=((a_dict.get("scan", {}) or {}).get("link", {}) or {}).get("rel"),
                        uri=((a_dict.get("scan", {}) or {}).get("link", {}) or {}).get("uri")
                    )
                ),
                status=a_dict.get("status"),
                last_sync=a_dict.get("lastSync"),
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_the_publish_last_scan_results_to_management_and_orchestration_status(project_id)
        else:
            raise UnknownHttpStatusError()

        return policy_finding_status

    def register_scan_report(self, scan_id, report_type):
        """
        Generate a new CxSAST scan report.

        Args:
            scan_id (int):
            report_type (str): Report type options are: PDF, RTF, CSV or XML

        Returns:
            :obj:`CxRegisterScanReportResponse`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        scan_report = None
        post_body = json.dumps(
            {
                "reportType": report_type,
                "scanId": scan_id
            }
        )

        r = requests.post(url=self.register_scan_report_url, data=post_body,
                          headers=AuthenticationAPI.AuthenticationAPI.auth_headers)

        if r.status_code == 202:
            a_dict = r.json()
            scan_report = CxRegisterScanReportResponse.CxRegisterScanReportResponse(
                report_id=a_dict.get("reportId"),
                links=CxRegisterScanReportResponse.CxRegisterScanReportResponse.Links(
                    report=CxLink.CxLink(
                        rel=((a_dict.get("links", {}) or {}).get("report", {}) or {}).get("rel"),
                        uri=((a_dict.get("links", {}) or {}).get("report", {}) or {}).get("uri")
                    ),
                    status=CxLink.CxLink(
                        rel=((a_dict.get("links", {}) or {}).get("status", {}) or {}).get("rel"),
                        uri=((a_dict.get("links", {}) or {}).get("status", {}) or {}).get("uri")
                    )
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.register_scan_report(scan_id, report_type)
        else:
            raise UnknownHttpStatusError()

        return scan_report

    def get_report_status_by_id(self, report_id):
        """
        Get the status of a generated report.


        Args:
            report_id (int):

        Returns:
            :obj:`CxScanReportStatus`

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError
        """
        report_status = None

        self.report_status_url = self.report_status_url.format(id=report_id)
        r = requests.get(url=self.report_status_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            a_dict = r.json()
            report_status = CxScanReportStatus.CxScanReportStatus(
                link=CxLink.CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                ),
                content_type=a_dict.get("contentType"),
                status=CxScanReportStatus.CxScanReportStatus.Status(
                    status_id=(a_dict.get("status", {}) or {}).get("id"),
                    value=(a_dict.get("status", {}) or {}).get("value")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_report_status_by_id(report_id)
        else:
            raise UnknownHttpStatusError()

        return report_status

    def get_report_by_id(self, report_id):
        """
        Get the specified report once generated.
        :param report_id:
        :return:

        Args:
            report_id (int):

        Returns:
            byte

        Raises:
            BadRequestError
            NotFoundError
            UnknownHttpStatusError

        """
        report_content = None
        self.report_url = self.report_url.format(id=report_id)
        r = requests.get(url=self.report_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == 200:
            # write r.content to file with "wb" mode
            report_content = r.content
        elif r.status_code == 204:
            pass
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_report_by_id(report_id)
        else:
            raise UnknownHttpStatusError()
        
        return report_content

    def is_scanning_finished(self, scan_id):
        """
        check if a scan is finished

        Args:
            scan_id (int):

        Returns:
            bool
        """
        is_finished = False

        scan_detail = self.get_sast_scan_details_by_scan_id(scan_id=scan_id)
        if scan_detail.status.name == "Finished":
            is_finished = True

        return is_finished

    def is_report_generation_finished(self, report_id):
        """
        check if a report generation is finished

        Args:
            report_id (int):

        Returns:

        """
        is_finished = False

        report_status = self.get_report_status_by_id(report_id)
        if report_status.status.value == "Created":
            is_finished = True

        return is_finished
