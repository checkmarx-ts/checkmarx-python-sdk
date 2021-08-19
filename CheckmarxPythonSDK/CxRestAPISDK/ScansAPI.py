# encoding: utf-8
import os
import copy
import requests
import json

from requests_toolbelt import MultipartEncoder

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, CREATED, NO_CONTENT, ACCEPTED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .sast.projects.dto import CxLink, CxProject, CxPreset
from .sast.engines.dto import CxEngineServer, CxEngineConfiguration
from .sast.scans.dto import CxSchedulingSettings, CxScanState, CxPolicyFindingsStatus, \
    CxResultsStatistics, CxPolicyFindingResponse, CxStatus, CxFinishedScanStatus, CxStatisticsResult, \
    CxCreateNewScanResponse, CxCreateScan, CxRegisterScanReportResponse, CxScanType, CxScanDetail, CxScanReportStatus, \
    CxDateAndTime, CxScanQueueDetail, CxScanStage, CxLanguageState, CxStatusDetail, CxScanSettings, \
    CxCreateScanSettingsResponse, CxEmailNotification, CxCreateScanSettingsRequestBody, CxLanguage, \
    CxScanResultAttackVectorByBFL, construct_attack_vector, construct_scan_result_node, CxScanResultLabelsFields, \
    CxScanStatistics, CxScanFileCountOfLanguage, CxLanguageStatistic, CxScanParsedFiles, CxScanParsedFilesMetric, \
    CxScanFailedQueries, CxScanFailedGeneralQueries, CxScanSucceededGeneralQueries


class ScansAPI(object):
    """
    scans API
    """

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
            project=CxProject(
                project_id=item.get("project", {}).get("id"),
                name=item.get("project", {}).get("name"),
                link=item.get("project", {}).get("link")
            ),
            status=CxStatus(
                status_id=item.get("status", {}).get("id"),
                name=item.get("status", {}).get("name"),
                details=CxStatusDetail(
                    stage=item.get("status", {}).get("details", {}).get("stage"),
                    step=item.get("status", {}).get("details", {}).get("step")
                )
            ),
            scan_type=CxScanType(
                scan_type_id=item.get("scanType", {}).get("id"),
                value=item.get("scanType", {}).get("value")
            ),
            comment=item.get("comment"),
            date_and_time=CxDateAndTime(
                started_on=(item.get("dateAndTime", {}) or {}).get("startedOn"),
                finished_on=(item.get("dateAndTime", {}) or {}).get("finishedOn"),
                engine_started_on=(item.get("dateAndTime", {}) or {}).get("engineStartedOn"),
                engine_finished_on=(item.get("dateAndTime", {}) or {}).get("engineFinishedOn")
            ),
            results_statistics=CxResultsStatistics(
                link=(item.get("resultsStatistics", {}) or {}).get("link")
            ),
            scan_state=CxScanState(
                path=(item.get("scanState", {}) or {}).get("path"),
                source_id=(item.get("scanState", {}) or {}).get("sourceId"),
                files_count=(item.get("scanState", {}) or {}).get("filesCount"),
                lines_of_code=(item.get("scanState", {}) or {}).get("linesOfCode"),
                failed_lines_of_code=(item.get("scanState", {}) or {}).get("failedLinesOfCode"),
                cx_version=(item.get("scanState", {}) or {}).get("cxVersion"),
                language_state_collection=[
                    CxLanguageState(
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
            engine_server=CxEngineServer(
                engine_server_id=(item.get("engineServer", {}) or {}).get("id"),
                name=(item.get("engineServer", {}) or {}).get("name"),
                link=(item.get("engineServer", {}) or {}).get("link"),
            ),
            finished_scan_status=CxFinishedScanStatus(
                scan_status_id=(item.get("finishedScanStatus", {}) or {}).get("id"),
                value=(item.get("finishedScanStatus", {}) or {}).get("value")
            ),
            partial_scan_reasons=item.get("partialScanReasons"),
            custom_fields=item.get("customFields")
        )

    def get_all_scans_for_project(self, project_id=None, scan_status=None, last=None, api_version="1.0"):
        """
        Get details of all SAST scans for a specific project.


        Args:
            project_id (int, optional): Unique Id of the project
            scan_status (str, optional): The current status of the scan
                        (1="New", 2="PreScan", 3="Queued", 4="Scanning", 6="PostScan", 7="Finished", 8="Canceled",
                        9="Failed", 10="SourcePullingAndDeployment", 1001="None").
            last (int):  Number of last scans to include.
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxScanDetail`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        all_scans_url = config.get("base_url") + "/cxrestapi/sast/scans"

        optionals = []
        if project_id:
            optionals.append("projectId={}".format(project_id))
        if scan_status:
            optionals.append("scanStatus={}".format(scan_status))
        if last:
            optionals.append("last={}".format(last))
        if optionals:
            all_scans_url += "?" + "&".join(optionals)

        r = requests.get(
            url=all_scans_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            all_scans = [
                self.__construct_scan(item) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_scans = self.get_all_scans_for_project(project_id, scan_status, last, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_scans

    def get_last_scan_id_of_a_project(self, project_id, only_finished_scans=False):
        """
        get the last scan id of a project

        Args:
            project_id (int): Unique Id of the project
            only_finished_scans (bool): True for only finished scans

        Returns:
            int: scan id
        """
        scan_id = None

        if project_id:
            all_scans_for_this_project = self.get_all_scans_for_project(project_id)

            if only_finished_scans:
                all_scans_for_this_project = filter(lambda scan: scan.status.name == "Finished",
                                                    all_scans_for_this_project)

            all_scans_for_this_project = sorted(all_scans_for_this_project,
                                                key=lambda scan: scan.id,
                                                reverse=True)
            if len(all_scans_for_this_project) > 0:
                scan_id = all_scans_for_this_project[0].id

        return scan_id

    def create_new_scan(self, project_id, is_incremental=False, is_public=True, force_scan=True, comment="",
                        custom_fields=None, api_version="1.0"):
        """
        Create a new SAST scan and assign it to a project.

        Args:
            project_id (int):  Unique Id of the project to be scanned
            is_incremental (boolean): Specifies whether the requested scan is incremental or full scan
            is_public (boolean):  Specifies whether the requested scan is public or private
            force_scan (boolean): Specifies whether the code should be scanned or not, regardless of whether changes
                                were made to the code since the last scan.
            comment (str): Specifies the scan comment.
            custom_fields (dict, optional): dict with key-value pairs, api_version must be "1.2"
                            e.g. {
                                    "key": "value"
                                 }
            api_version (str, optional):

        Returns:
            :obj:`CxCreateNewScanResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        all_scans_url = config.get("base_url") + "/cxrestapi/sast/scans"

        post_body = CxCreateScan(
            project_id, is_incremental, is_public, force_scan, comment, custom_fields=custom_fields
        ).get_post_data()

        r = requests.post(
            url=all_scans_url,
            data=post_body,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            a_dict = r.json()
            scan = CxCreateNewScanResponse(
                scan_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            scan = self.create_new_scan(project_id, is_incremental, is_public, force_scan, comment,
                                        custom_fields=custom_fields,
                                        api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return scan

    def get_sast_scan_details_by_scan_id(self, scan_id, api_version="1.0"):
        """
        Get details of a specific SAST scan.

        Args:
            scan_id (int): Unique Id of the scan
            api_version (str, optional):

        Returns:
            :obj:`CxScanDetail`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        sast_scan_url = config.get("base_url") + "/cxrestapi/sast/scans/{id}".format(id=scan_id)

        r = requests.get(
            url=sast_scan_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            item = r.json()
            scan_detail = self.__construct_scan(item)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            scan_detail = self.get_sast_scan_details_by_scan_id(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return scan_detail

    def add_or_update_a_comment_by_scan_id(self, scan_id, comment, api_version="1.0"):
        """
        Add a new comment or update an existing comment according to the scan Id.
        This action can only be applied to finished scans.

        Args:
            scan_id (int): Unique Id of a specific scan
            comment (str): Specifies the comment content
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        sast_scan_url = config.get("base_url") + "/cxrestapi/sast/scans/{id}".format(id=scan_id)

        patch_data = json.dumps(
            {
                "comment": comment
            }
        )
        r = requests.patch(
            url=sast_scan_url,
            data=patch_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.add_or_update_a_comment_by_scan_id(scan_id, comment, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def delete_scan_by_scan_id(self, scan_id, api_version="1.0"):
        """
        Delete specific SAST scan according to scan Id.
        This action can only be applied to finished scans.

        Args:
            scan_id (int): Unique Id of the scan
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        sast_scan_url = config.get("base_url") + "/cxrestapi/sast/scans/{id}".format(id=scan_id)

        r = requests.delete(
            url=sast_scan_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == ACCEPTED:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.delete_scan_by_scan_id(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_statistics_results_by_scan_id(self, scan_id, api_version="1.0"):
        """
        Get statistic results for a specific scan.
        This action can only be applied to finished scans.

        Args:
            scan_id (int): Unique Id of the scan
            api_version (str, optional):

        Returns:
            :obj:`CxStatisticsResult`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        statistics_results_url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/resultsStatistics".format(
            id=scan_id)

        r = requests.get(
            url=statistics_results_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            item = r.json()
            statistics = CxStatisticsResult(
                high_severity=item.get("highSeverity"),
                medium_severity=item.get("mediumSeverity"),
                low_severity=item.get("lowSeverity"),
                info_severity=item.get("infoSeverity"),
                statistics_calculation_date=item.get("statisticsCalculationDate")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            statistics = self.get_statistics_results_by_scan_id(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return statistics

    @staticmethod
    def __construct_scan_queue_detail(item):
        return CxScanQueueDetail(
            scan_queue_detail_id=item.get("id"),
            stage=CxScanStage(
                scan_stage_id=(item.get("stage", {}) or {}).get("id"),
                value=(item.get("stage", {}) or {}).get("value")
            ),
            stage_details=item.get("stageDetails"),
            step_details=item.get("stepDetails"),
            project=CxProject(
                project_id=(item.get("project", {}) or {}).get("id"),
                name=(item.get("project", {}) or {}).get("name"),
                link=CxLink(
                    rel=((item.get("project", {}) or {}).get("link", {}) or {}).get("rel"),
                    uri=((item.get("project", {}) or {}).get("link", {}) or {}).get("uri")
                )
            ),
            engine=CxEngineServer(
                engine_server_id=(item.get("engine", {}) or {}).get("id"),
                link=CxLink(
                    rel=((item.get("engine", {}) or {}).get("link", {}) or {}).get("rel"),
                    uri=((item.get("engine", {}) or {}).get("link", {}) or {}).get("uri")
                )
            ),
            languages=[
                CxLanguage(
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

    def get_scan_queue_details_by_scan_id(self, scan_id, api_version="1.0"):
        """
        Get details of a specific CxSAST scan in the scan queue according to the scan Id.

        Args:
            scan_id (int): Unique Id of the scan
            api_version (str, optional):

        Returns:
            :obj:`CxScanQueueDetail`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        scans_queue_url = config.get("base_url") + "/cxrestapi/sast/scansQueue/{id}".format(id=scan_id)

        r = requests.get(
            url=scans_queue_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            item = r.json()
            scan_queue_details = self.__construct_scan_queue_detail(item)
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            scan_queue_details = self.get_scan_queue_details_by_scan_id(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return scan_queue_details

    def update_queued_scan_status_by_scan_id(self, scan_id, status_id=None, status_value=None, api_version="1.0"):
        """
        Update (Cancel) a running scan in the queue according to the scan Id.


        Args:
            scan_id (int):  Unique Id of a specific scan in the queue
            status_id (int): Unique Id of the status
            status_value (str): Requested scan status in the queue. Status option include Cancelled.
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        scans_queue_url = config.get("base_url") + "/cxrestapi/sast/scansQueue/{id}".format(id=scan_id)

        patch_data = json.dumps({
            "status": "Canceled"
        })

        r = requests.patch(
            url=scans_queue_url,
            data=patch_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_queued_scan_status_by_scan_id(scan_id, status_id, status_value,
                                                                      api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_all_scan_details_in_queue(self, project_id=None, api_version="1.0"):
        """
        GET /sast/scansQueue Get details of all SAST scans in the scans queue.

        Args:
            project_id (int): Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxScanQueueDetail`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        all_scan_queue_url = config.get("base_url") + "/cxrestapi/sast/scansQueue"

        if project_id:
            all_scan_queue_url += "?projectId=" + str(project_id)

        r = requests.get(
            url=all_scan_queue_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            all_scan_details_in_queue = [self.__construct_scan_queue_detail(item) for item in a_list]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            all_scan_details_in_queue = self.get_all_scan_details_in_queue(project_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_scan_details_in_queue

    def get_scan_settings_by_project_id(self, project_id, api_version="1.0"):
        """
        Get scan settings by project Id.

        Args:
            project_id (int): Unique Id of the project
            api_version (str, optional):

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        scan_settings_url = config.get("base_url") + "/cxrestapi/sast/scanSettings/{projectId}".format(
            projectId=project_id)

        r = requests.get(
            url=scan_settings_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            scan_settings = CxScanSettings(
                project=CxProject(
                    project_id=(a_dict.get("project", {}) or {}).get("id"),
                    link=CxLink(
                        rel=(a_dict.get("project", {}) or {}).get("link", {}).get("rel"),
                        uri=(a_dict.get("project", {}) or {}).get("link", {}).get("uri")
                    )
                ),
                preset=CxPreset(
                    preset_id=(a_dict.get("preset", {}) or {}).get("id"),
                    link=CxLink(
                        rel=(a_dict.get("preset", {}) or {}).get("link", {}).get("rel"),
                        uri=(a_dict.get("preset", {}) or {}).get("link", {}).get("uri")
                    )
                ),
                engine_configuration=CxEngineConfiguration(
                    engine_configuration_id=(a_dict.get("engineConfiguration", {}) or {}).get("id"),
                    link=CxLink(
                        rel=(a_dict.get("engineConfiguration", {}) or {}).get("link", {}).get("rel"),
                        uri=(a_dict.get("engineConfiguration", {}) or {}).get("link", {}).get("uri")
                    )
                ),
                post_scan_action=a_dict.get("postScanAction"),
                email_notifications=CxEmailNotification(
                    failed_scan=(a_dict.get("emailNotifications", {}) or {}).get("failedScan"),
                    before_scan=(a_dict.get("emailNotifications", {}) or {}).get("beforeScan"),
                    after_scan=(a_dict.get("emailNotifications", {}) or {}).get("afterScan"),
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            scan_settings = self.get_scan_settings_by_project_id(project_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return scan_settings

    def define_sast_scan_settings(self, project_id, preset_id, engine_configuration_id=1, post_scan_action_id=None,
                                  failed_scan_emails=None, before_scan_emails=None, after_scan_emails=None,
                                  api_version="1.0"):
        """
        Define the SAST scan settings according to a project (preset and engine configuration).

        Args:
            project_id (int): Unique Id of the project
            preset_id (int):  Unique Id of the preset
            engine_configuration_id (int): Unique Id of the engine configuration
            post_scan_action_id (int, optional): Unique Id of the post scan action
            before_scan_emails (:obj:`list` of :obj:`str`, optional): Specifies the email to send the pre-scan message
            failed_scan_emails (:obj:`list` of :obj:`str`, optional): Specifies the email to send the scan failure
                                                                        message
            after_scan_emails (:obj:`list` of :obj:`str`, optional): Specifies the email to send the post-scan message
            api_version (str, optional):

        Returns:
            :obj:`CxCreateScanSettingsResponse`

        Raises：
            BadRequestError
            NotFoundError
            CxError
        """
        all_scan_settings_url = config.get("base_url") + "/cxrestapi/sast/scanSettings"

        post_body_data = CxCreateScanSettingsRequestBody(
            project_id=project_id,
            preset_id=preset_id,
            engine_configuration_id=engine_configuration_id,
            post_scan_action_id=post_scan_action_id,
            failed_scan_emails=failed_scan_emails,
            before_scan_emails=before_scan_emails,
            after_scan_emails=after_scan_emails
        ).get_post_data()
        r = requests.post(
            url=all_scan_settings_url,
            data=post_body_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            sast_scan_settings = CxCreateScanSettingsResponse(
                scan_setting_response_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            sast_scan_settings = self.define_sast_scan_settings(project_id, preset_id, engine_configuration_id,
                                                                post_scan_action_id,
                                                                failed_scan_emails, before_scan_emails,
                                                                after_scan_emails, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return sast_scan_settings

    def update_sast_scan_settings(self, project_id, preset_id=1, engine_configuration_id=1, post_scan_action_id=None,
                                  failed_scan_emails=None, before_scan_emails=None, after_scan_emails=None,
                                  api_version="1.0"):
        """
        Update the SAST scan settings for a project
        (preset, engine configuration, custom actions and email notifications).

        Args:
            project_id (int): Unique Id of the project
            preset_id (int): Unique Id of the preset
            engine_configuration_id (int):  Unique Id of the engine configuration
            post_scan_action_id (int, optional):  Unique Id of the post scan action
            failed_scan_emails (:obj:`list` of :obj:`str`, optional): Specifies the email to send the scan failure
                                                                        notification
            before_scan_emails (:obj:`list` of :obj:`str`, optional): Specifies the email to send the pre-scan
                                                                    notification
            after_scan_emails (:obj:`list` of :obj:`str`, optional): Specifies the email to send the post-scan
                                                                    notification
            api_version (str, optional):

        Returns:
            :obj:`CxCreateScanSettingsResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        all_scan_settings_url = config.get("base_url") + "/cxrestapi/sast/scanSettings"

        post_body_data = CxCreateScanSettingsRequestBody(
            project_id=project_id,
            preset_id=preset_id,
            engine_configuration_id=engine_configuration_id,
            post_scan_action_id=post_scan_action_id,
            failed_scan_emails=failed_scan_emails,
            before_scan_emails=before_scan_emails,
            after_scan_emails=after_scan_emails
        ).get_post_data()
        r = requests.put(
            url=all_scan_settings_url,
            data=post_body_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            sast_scan_settings = CxCreateScanSettingsResponse(
                scan_setting_response_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            sast_scan_settings = self.update_sast_scan_settings(project_id, preset_id, engine_configuration_id,
                                                                post_scan_action_id,
                                                                failed_scan_emails, before_scan_emails,
                                                                after_scan_emails, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return sast_scan_settings

    def define_sast_scan_scheduling_settings(self, project_id, schedule_type, schedule_days, schedule_time,
                                             api_version="1.0"):
        """
        Define SAST scan scheduling settings for a project.


        Args:
            project_id (int):  Unique Id of the project
            schedule_type (str): Specifies the schedule type (none or weekly)
            schedule_days (:obj:`list` of :obj:`str`):  Specifies the day(s) to perform the scan
                                    (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday).
                                    Comma separate days can also be defined
            schedule_time (str): Specifies the time(s) to perform the scan (hh:mm)
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        schedule_settings_url = config.get("base_url") + "/cxrestapi/sast/project/{projectId}/scheduling".format(
            projectId=project_id)

        post_body_data = CxSchedulingSettings(
            schedule_type=schedule_type,
            schedule_days=schedule_days,
            schedule_time=schedule_time
        ).get_post_data()

        r = requests.put(
            url=schedule_settings_url,
            data=post_body_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.define_sast_scan_scheduling_settings(project_id, schedule_type, schedule_days,
                                                                      schedule_time, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def assign_ticket_to_scan_results(self, results_id, ticket_id, api_version="1.0"):
        """
        Assign ticket to scan results according to scan results and ticket Id.

        Args:
            results_id (str): Unique Id of the result. ResultsId is made up of the Scan Id and Path Id (example:
                                    ScanId = 1000025, PathId = 12, therefore ResultsId = 1000025-12)
            ticket_id (str): Unique Id of the ticket.
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        post_body_data = json.dumps(
            {
                "resultsId": [results_id],
                "ticketId": ticket_id
            }
        )

        scan_results_ticket_url = config.get("base_url") + "/cxrestapi/sast/results/tickets"

        r = requests.post(
            url=scan_results_ticket_url,
            data=post_body_data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.assign_ticket_to_scan_results(results_id, ticket_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def publish_last_scan_results_to_management_and_orchestration_by_project_id(self, project_id, api_version="1.0"):
        """
        Publish last scan results to Management and Orchestration for a specific project
        (only for policy management evaluation in v8.9.0).

        Args:
            project_id (int):  Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxPolicyFindingResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        policy_findings_url = config.get("base_url") + "/cxrestapi/sast/projects/{id}/publisher/policyFindings".format(
            id=project_id)

        r = requests.post(
            url=policy_findings_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == CREATED:
            a_dict = r.json()
            policy_finding_response = CxPolicyFindingResponse(
                policy_finding_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            policy_finding_response = self.publish_last_scan_results_to_management_and_orchestration_by_project_id(
                project_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return policy_finding_response

    def get_the_publish_last_scan_results_to_management_and_orchestration_status(self, project_id, api_version="1.0"):
        """
        Get the status of publish last scan results to Management and Orchestration layer for a specific project.

        Args:
            project_id (int): Unique Id of the project
            api_version (str, optional):

        Returns:
            :obj:`CxPolicyFindingsStatus`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        policy_findings_status_url = config.get(
            "base_url") + "/cxrestapi/sast/projects/{id}/publisher/policyFindings/status".format(
            id=project_id
        )

        r = requests.get(
            url=policy_findings_status_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            policy_finding_status = CxPolicyFindingsStatus(
                project=CxProject(
                    project_id=(a_dict.get("project", {}) or {}).get("id"),
                    link=CxLink(
                        rel=((a_dict.get("project", {}) or {}).get("link", {}) or {}).get("rel"),
                        uri=((a_dict.get("project", {}) or {}).get("link", {}) or {}).get("uri")
                    )
                ),
                scan=CxCreateNewScanResponse(
                    scan_id=(a_dict.get("scan", {}) or {}).get("id"),
                    link=CxLink(
                        rel=((a_dict.get("scan", {}) or {}).get("link", {}) or {}).get("rel"),
                        uri=((a_dict.get("scan", {}) or {}).get("link", {}) or {}).get("uri")
                    )
                ),
                status=a_dict.get("status"),
                last_sync=a_dict.get("lastSync"),
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            policy_finding_status = self.get_the_publish_last_scan_results_to_management_and_orchestration_status(
                project_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return policy_finding_status

    def get_short_vulnerability_description_for_a_scan_result(self, scan_id, path_id, api_version="1.0"):
        """
        Get the short version of a vulnerability description for a specific scan result.
        This action can only be applied to finished scans.

        Args:
            scan_id (int): Unique Id of the scan
            path_id (int): Unique Id of the result path
            api_version (str, optional):

        Returns:
            str
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/results/{pathId}/shortDescription".format(
            id=scan_id, pathId=path_id
        )

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            short_description = a_dict.get("shortDescription")
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError(r.text)
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            short_description = self.get_short_vulnerability_description_for_a_scan_result(scan_id, path_id,
                                                                                           api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return short_description

    def register_scan_report(self, scan_id, report_type, api_version="1.0"):
        """
        Generate a new CxSAST scan report.
        This action can only be applied to finish scans.

        Args:
            scan_id (int): Unique Id of the scan
            report_type (str): Report type options are: PDF, RTF, CSV or XML
            api_version (str, optional):

        Returns:
            :obj:`CxRegisterScanReportResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        post_body = json.dumps(
            {
                "reportType": report_type,
                "scanId": scan_id
            }
        )

        register_scan_report_url = config.get("base_url") + "/cxrestapi/reports/sastScan"

        r = requests.post(
            url=register_scan_report_url,
            data=post_body,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == ACCEPTED:
            a_dict = r.json()
            scan_report = CxRegisterScanReportResponse(
                report_id=a_dict.get("reportId"),
                links=CxRegisterScanReportResponse.Links(
                    report=CxLink(
                        rel=((a_dict.get("links", {}) or {}).get("report", {}) or {}).get("rel"),
                        uri=((a_dict.get("links", {}) or {}).get("report", {}) or {}).get("uri")
                    ),
                    status=CxLink(
                        rel=((a_dict.get("links", {}) or {}).get("status", {}) or {}).get("rel"),
                        uri=((a_dict.get("links", {}) or {}).get("status", {}) or {}).get("uri")
                    )
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            scan_report = self.register_scan_report(scan_id, report_type, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return scan_report

    def get_report_status_by_id(self, report_id, api_version="1.0"):
        """
        Get the status of a generated report.


        Args:
            report_id (int): Unique Id of the report
            api_version (str, optional):

        Returns:
            :obj:`CxScanReportStatus`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """

        report_status_url = config.get("base_url") + "/cxrestapi/reports/sastScan/{id}/status".format(id=report_id)

        r = requests.get(
            url=report_status_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            report_status = CxScanReportStatus(
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                ),
                content_type=a_dict.get("contentType"),
                status=CxScanReportStatus.Status(
                    status_id=(a_dict.get("status", {}) or {}).get("id"),
                    value=(a_dict.get("status", {}) or {}).get("value")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            report_status = self.get_report_status_by_id(report_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return report_status

    def get_report_by_id(self, report_id, api_version="1.0"):
        """
        Get the specified report once generated.

        Args:
            report_id (int): Unique Id of the report
            api_version (str, optional):

        Returns:
            byte

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        report_url = config.get("base_url") + "/cxrestapi/reports/sastScan/{id}".format(id=report_id)

        r = requests.get(
            url=report_url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            # write r.content to file with "wb" mode
            report_content = r.content
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            report_content = self.get_report_by_id(report_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return report_content

    def is_scanning_finished(self, scan_id):
        """
        check if a scan is finished

        Args:
            scan_id (int): unique id of a scan

        Returns:
            boolean
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
            report_id (int): unique id of a report

        Returns:

        """
        is_finished = False

        report_status = self.get_report_status_by_id(report_id)
        if report_status.status.value == "Created":
            is_finished = True

        return is_finished

    def get_scan_results_of_a_specific_query(self, scan_id, query_version_code, api_version="1.0"):
        """
        Get the scan results for a specific query in Attack Vector format. This format includes all nodes.

        Args:
            scan_id (int):
            query_version_code (int):
            api_version (str, optional):

        Returns:
            attack_vectors (`list` of `CxScanResultAttackVector`)
        """

        url = config.get("base_url") + ("/cxrestapi/sast/results/attack-vectors"
                                        "?scanId={scanId}&queryVersion={queryVersion}").format(
            scanId=scan_id, queryVersion=query_version_code
        )

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            vectors = r.json().get('attackVectors')
            attack_vectors = [
                construct_attack_vector(ac) for ac in vectors
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            attack_vectors = self.get_scan_results_of_a_specific_query(scan_id, query_version_code,
                                                                       api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return attack_vectors

    def get_scan_results_for_a_specific_query_group_by_best_fix_location(self, scan_id, query_version_code,
                                                                         api_version="1.0"):
        """

        Args:
            scan_id (int):
            query_version_code (int):
            api_version (str, optional):

        Returns:
           attack_vectors_by_bfl  (`list` of `CxScanResultAttackVectorByBFL`)
        """

        url = config.get("base_url") + ("/cxrestapi/sast/results/attack-vectors-by-bfl"
                                        "?scanId={scanId}&queryVersion={queryVersion}").format(
            scanId=scan_id, queryVersion=query_version_code
        )

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )
        if r.status_code == OK:
            attack_vectors_by_bfl = r.json().get("attackVectorsByBFL")
            attack_vectors_by_bfl = [
                CxScanResultAttackVectorByBFL(
                    scan_id=ac_bfl.get("scanId"),
                    query_version_code=ac_bfl.get("queryVersion"),
                    best_fix_location_node=construct_scan_result_node(ac_bfl.get("bestFixLocationNode")),
                    attack_vectors=[construct_attack_vector(ac) for ac in ac_bfl.get("attackVectors")]
                ) for ac_bfl in attack_vectors_by_bfl
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            attack_vectors_by_bfl = self.get_scan_results_for_a_specific_query_group_by_best_fix_location(
                scan_id, query_version_code, api_version=api_version
            )
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return attack_vectors_by_bfl

    def update_scan_result_labels_fields(self, scan_id, result_id, state, severity, user_assignment, comment,
                                         api_version="1.0"):
        """

        Args:
            scan_id (int):
            result_id (int):
            state (int, optional):  0 (To Verify),
                                    1 (Not Exploitable),
                                    2 (Confirmed),
                                    3 (Urgent),
                                    4 (Proposed Not Exploitable)
            severity (int, optional): 1 (Low, optional), 2 (Medium), 3 (High)
            user_assignment (str, optional):
            comment (str, optional):
            api_version (str, optional):

        Returns:
            is_successful (bool)
        """
        from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_version_number_as_int
        version = get_version_number_as_int()

        label_url = "/cxrestapi/sast/scans/{scanId}/results/{resultId}"
        if version >= 940:
            label_url = "/cxrestapi//sast/scans/{scanId}/results/{resultId}/labels"

        url = config.get("base_url") + label_url.format(
            scanId=scan_id, resultId=result_id)

        data = json.dumps({
            "state": state,
            "severity": severity,
            "userAssignment": user_assignment,
            "comment": comment,
        })

        r = requests.patch(
            url=url,
            data=data,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            is_successful = self.update_scan_result_labels_fields(scan_id, result_id, state, severity, user_assignment,
                                                                  comment, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def create_new_scan_with_settings(self, project_id, preset_id, zipped_source_file_path,
                                      override_project_setting=False,
                                      is_incremental=False,
                                      is_public=False, force_scan=True, comment="", engine_configuration_id=0,
                                      custom_fields=None, post_scan_action_id=None,
                                      api_version="1.0"):
        """

        Args:
            project_id (int):
            preset_id (int):
            zipped_source_file_path (str):
            override_project_setting (booL):
            is_incremental (bool):
            is_public (bool):
            force_scan (bool):
            comment (str):
            engine_configuration_id (int):
            custom_fields (dict, optional):   api_version must be "1.2"
                            e.g. {
                                    "key": "value"
                                 }
            post_scan_action_id (int, optional):
            api_version (str, optional):

        Returns:



        """
        attachments_url = config.get("base_url") + "/cxrestapi/sast/scanWithSettings"

        headers = copy.deepcopy(authHeaders.get_headers(api_version=api_version))

        file_name = os.path.basename(zipped_source_file_path)

        if not os.path.exists(zipped_source_file_path):
            print("zipped_source_file_path not exist: {}".format(zipped_source_file_path))
            return None

        fields = {
            "projectId": str(project_id),
            "overrideProjectSetting": str(override_project_setting),
            "isIncremental": str(is_incremental),
            "isPublic": str(is_public),
            "forceScan": str(force_scan),
            "comment": str(comment),
            "presetId": str(preset_id),
            "engineConfigurationId": str(engine_configuration_id),
            "zippedSource": (file_name, open(zipped_source_file_path, 'rb'), "application/zip")
        }

        if custom_fields:
            fields.update({"customFields": json.dumps(custom_fields)})

        if post_scan_action_id:
            fields.update({"postScanActionId": str(post_scan_action_id)})

        m = MultipartEncoder(
            fields=fields
        )
        headers.update({"Content-Type": m.content_type})

        r = requests.post(
            url=attachments_url,
            headers=headers,
            data=m,
            verify=config.get("verify")
        )
        if r.status_code == CREATED:
            a_dict = r.json()
            scan = CxCreateNewScanResponse(
                scan_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            scan = self.create_new_scan_with_settings(project_id, preset_id, zipped_source_file_path,
                                                      override_project_setting,
                                                      is_incremental,
                                                      is_public, force_scan, comment, engine_configuration_id,
                                                      custom_fields=custom_fields,
                                                      post_scan_action_id=post_scan_action_id,
                                                      api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return scan

    def get_scan_result_labels_fields(self, scan_id, result_id, api_version="1.0"):
        """

        Args:
            scan_id (int): Unique Id of a scan
            result_id (int): Unique Id of the result path
            api_version (str, optional):

        Returns:

        """
        label_url = "/cxrestapi/sast/scans/{scanId}/results/{resultId}/labels"

        url = config.get("base_url") + label_url.format(
            scanId=scan_id, resultId=result_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            fields = CxScanResultLabelsFields(
                state=a_dict.get("state"),
                severity=a_dict.get("severity"),
                user_assignment=a_dict.get("userAssignment"),
                comment=a_dict.get("comment")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            fields = self.get_scan_result_labels_fields(scan_id, result_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return fields

    def get_scan_logs(self, scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            binary string, contains zip file content
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/logs".format(id=scan_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            logs = r.content
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            logs = self.get_scan_logs(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return logs

    def get_basic_metrics_of_a_scan(self, scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanStatistics`
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/statistics".format(id=scan_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            statistics = CxScanStatistics(
                statistics_id=item.get("id"),
                scan_id=item.get("scanId"),
                scan_status=item.get("scanStatus"),
                product_version=item.get("productVersion"),
                engine_version=item.get("engineVersion"),
                memory_peak_in_mb=item.get("memoryPeakInMB"),
                virtual_memory_peak_in_mb=item.get("virtualMemoryPeakInMB"),
                is_incremental_scan=item.get("isIncrementalScan"),
                results_count=item.get("resultsCount"),
                total_unscanned_files_count=item.get("totalUnScannedFilesCount"),
                file_count_of_detected_but_not_scanned_languages=[
                    CxScanFileCountOfLanguage(
                        language=key,
                        file_count=value,
                    )
                    for key, value in item.get("fileCountOfDetectedButNotScannedLanguages", {}).items()
                ],
                total_filtered_parsed_loc=item.get("totalFilteredParsedLOC"),
                total_unfiltered_parsed_loc=item.get("totalUnFilteredParsedLOC"),
                language_statistics=[
                    CxLanguageStatistic(
                        language=key,
                        parsed_successfully_count=value.get("parsedFiles", {}).get("parsedSuccessfullyCount"),
                        parsed_unsuccessfully_count=value.get("parsedFiles", {}).get("parsedUnsuccessfullyCount"),
                        parsed_partially_count=value.get("parsedFiles", {}).get("parsedPartiallyCount"),
                        successful_loc=value.get("scannedLOCPerLanguage", {}).get("successfulLOC"),
                        unsuccessful_loc=value.get("scannedLOCPerLanguage", {}).get("unsuccessfulLOC"),
                        scanned_successfully_loc_percentage=value.get("scannedLOCPerLanguage",
                                                                      {}).get("scannedSuccessfullyLOCPercentage"),
                        count_of_dom_objects=value.get("countOfDomObjects")
                    )
                    for key, value in item.get("languageStatistics").items()
                ],
                exclusion_folders_pattern=item.get("exclusionFoldersPattern"),
                exclusion_files_pattern=item.get("exclusionFilesPattern"),
                failed_queries_count=item.get("failedQueriesCount"),
                succeeded_general_queries_count=item.get("generalQueries", {}).get("succeededGeneralQueriesCount"),
                failed_general_queries_count=item.get("generalQueries", {}).get("failedGeneralQueriesCount"),
                failed_stages=item.get("failedStages"),
                engine_operating_system=item.get("engineOperatingSystem"),
                engine_pack_version=item.get("enginePackVersion"),
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            statistics = self.get_basic_metrics_of_a_scan(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return statistics

    def get_parsed_files_metrics_of_a_scan(self, scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanParsedFiles`
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/parsedFiles".format(id=scan_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            parsed_files = CxScanParsedFiles(
                scan_id=item.get("id"),
                scanned_files_per_language=[
                    CxScanParsedFilesMetric(
                        language=key,
                        parsed_successfully=value.get("parsedSuccessfully"),
                        parsed_unsuccessfully=value.get("parsedUnsuccessfully"),
                        parsed_partially=value.get("parsedPartially")
                    )
                    for key, value in item.get("scannedFilesPerLanguage").items()
                ]
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            parsed_files = self.get_parsed_files_metrics_of_a_scan(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return parsed_files

    def get_failed_queries_metrics_of_a_scan(self, scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanFailedQueries`
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/failedQueries".format(id=scan_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            failed_queries = CxScanFailedQueries(
                scan_id=item.get("id"),
                failed_queries=item.get("failedQueries")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            failed_queries = self.get_failed_queries_metrics_of_a_scan(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return failed_queries

    def get_failed_general_queries_metrics_of_a_scan(self, scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanFailedGeneralQueries`
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/failedGeneralQueries".format(id=scan_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            failed_general_queries = CxScanFailedGeneralQueries(
                scan_id=item.get("id"),
                failed_general_queries=item.get("failedGeneralQueries")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            failed_general_queries = self.get_failed_general_queries_metrics_of_a_scan(scan_id, api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return failed_general_queries

    def get_succeeded_general_queries_metrics_of_a_scan(self, scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanSucceededGeneralQueries`
        """
        url = config.get("base_url") + "/cxrestapi/sast/scans/{id}/succeededGeneralQueries".format(id=scan_id)

        r = requests.get(
            url=url,
            headers=authHeaders.get_headers(api_version=api_version),
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json()
            succeeded_general_queries = CxScanSucceededGeneralQueries(
                scan_id=item.get("id"),
                general_queries_result_count=item.get("generalQueriesResultCount")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            succeeded_general_queries = self.get_succeeded_general_queries_metrics_of_a_scan(scan_id,
                                                                                             api_version=api_version)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return succeeded_general_queries
