# encoding: utf-8
import os
import json
from os.path import normpath, exists, abspath

from requests_toolbelt import MultipartEncoder
from .httpRequests import get_request, post_request, put_request, patch_request, delete_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK, CREATED, NO_CONTENT, ACCEPTED
from .sast.projects.dto import CxLink, CxProject, CxPreset
from .sast.engines.dto import CxEngineServer, CxEngineConfiguration
from .sast.scans.dto import CxScanState, CxPolicyFindingsStatus, \
    CxResultsStatistics, CxPolicyFindingResponse, CxStatus, CxFinishedScanStatus, CxStatisticsResult, \
    CxCreateNewScanResponse, CxRegisterScanReportResponse, CxScanType, CxScanDetail, CxScanReportStatus, \
    CxDateAndTime, CxScanQueueDetail, CxScanStage, CxLanguageState, CxStatusDetail, CxScanSettings, \
    CxCreateScanSettingsResponse, CxEmailNotification, CxLanguage, \
    CxScanResultAttackVectorByBFL, construct_attack_vector, construct_scan_result_node, CxScanResultLabelsFields, \
    CxScanStatistics, CxScanFileCountOfLanguage, CxLanguageStatistic, CxScanParsedFiles, CxScanParsedFilesMetric, \
    CxScanFailedQueries, CxScanFailedGeneralQueries, CxScanSucceededGeneralQueries


class ScansAPI(object):
    """
    scans API
    """

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

    @staticmethod
    def get_all_scans_for_project(project_id=None, scan_status=None, last=None, api_version="1.0"):
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
        result = []
        relative_url = "/cxrestapi/sast/scans"
        optionals = []
        if project_id:
            optionals.append("projectId={}".format(project_id))
        if scan_status:
            optionals.append("scanStatus={}".format(scan_status))
        if last:
            optionals.append("last={}".format(last))
        if optionals:
            relative_url += "?" + "&".join(optionals)

        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                ScansAPI.__construct_scan(item) for item in response.json()
            ]
        return result

    @staticmethod
    def get_last_scan_id_of_a_project(project_id, only_finished_scans=False, only_completed_scans=True,
                                      only_real_scans=True, only_full_scans=True, only_public_scans=True):
        """
        get the last scan id of a project

        Args:
            project_id (int): Unique Id of the project
            only_finished_scans (bool): True for only finished scans
            only_completed_scans (bool): The finishedScanStatus could be Completed or Partial, True for Completed
            only_real_scans (bool): There could be attempted scans, which changed the date of the scan start,
                       but was never performed because there was no change in the code. For field dateAndTime, if the
                       startedOn is different from finishedOn, it is a real scan
            only_full_scans (bool): True for only full scans
            only_public_scans (bool): True for only public scans

        Returns:
            int: scan id
        """
        scan_id = None

        if not project_id:
            return scan_id

        all_scans_for_this_project = ScansAPI.get_all_scans_for_project(project_id)

        if only_finished_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.status.name == "Finished",
                all_scans_for_this_project
            )
        if only_completed_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.finished_scan_status.value == 'Completed',
                all_scans_for_this_project
            )

        if only_real_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.date_and_time.started_on != scan.date_and_time.finished_on,
                all_scans_for_this_project
            )

        if only_full_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.is_incremental is False,
                all_scans_for_this_project
            )

        if only_public_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.is_public is True,
                all_scans_for_this_project
            )

        all_scans_for_this_project = sorted(all_scans_for_this_project,
                                            key=lambda scan: scan.id,
                                            reverse=True)
        if len(all_scans_for_this_project) > 0:
            scan_id = all_scans_for_this_project[0].id

        return scan_id

    @staticmethod
    def create_new_scan(project_id, is_incremental=False, is_public=True, force_scan=True, comment="",
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
        result = None
        relative_url = "/cxrestapi/sast/scans"
        post_data = json.dumps(
            {
                "projectId": project_id,
                "isIncremental": is_incremental,
                "isPublic": is_public,
                "forceScan": force_scan,
                "comment": comment,
                "customFields": custom_fields
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxCreateNewScanResponse(
                scan_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def get_sast_scan_details_by_scan_id(scan_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = ScansAPI.__construct_scan(item)
        return result

    @staticmethod
    def add_or_update_a_comment_by_scan_id(scan_id, comment, api_version="1.0"):
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
        result = False
        relative_url = "/cxrestapi/sast/scans/{id}".format(id=scan_id)
        patch_data = json.dumps(
            {
                "comment": comment
            }
        )
        response = patch_request(relative_url=relative_url, data=patch_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def delete_scan_by_scan_id(scan_id, api_version="1.0"):
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
        result = False
        relative_url = "/cxrestapi/sast/scans/{id}".format(id=scan_id)
        response = delete_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            result = True
        return result

    @staticmethod
    def get_statistics_results_by_scan_id(scan_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/resultsStatistics".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxStatisticsResult(
                high_severity=item.get("highSeverity"),
                medium_severity=item.get("mediumSeverity"),
                low_severity=item.get("lowSeverity"),
                info_severity=item.get("infoSeverity"),
                statistics_calculation_date=item.get("statisticsCalculationDate")
            )
        return result

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

    @staticmethod
    def get_scan_queue_details_by_scan_id(scan_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/sast/scansQueue/{id}".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = ScansAPI.__construct_scan_queue_detail(item)
        return result

    @staticmethod
    def update_queued_scan_status_by_scan_id(scan_id, api_version="1.0"):
        """
        Update (Cancel) a running scan in the queue according to the scan Id.


        Args:
            scan_id (int):  Unique Id of a specific scan in the queue
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/sast/scansQueue/{id}".format(id=scan_id)
        patch_data = json.dumps({
            "status": "Canceled"
        })
        response = patch_request(relative_url=relative_url, data=patch_data, headers=get_headers(api_version))
        if response.status_code == OK:
            result = True
        return result

    @staticmethod
    def get_all_scan_details_in_queue(project_id=None, api_version="1.0"):
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
        result = []
        relative_url = "/cxrestapi/sast/scansQueue"
        if project_id:
            relative_url += "?projectId=" + str(project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [ScansAPI.__construct_scan_queue_detail(item) for item in response.json()]
        return result

    @staticmethod
    def get_scan_settings_by_project_id(project_id, api_version="1.0"):
        """
        Get scan settings by project Id.

        Args:
            project_id (int): Unique Id of the project
            api_version (str, optional):

        Returns:
            CxScanSettings

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/sast/scanSettings/{projectId}".format(projectId=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxScanSettings(
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
        return result

    @staticmethod
    def define_sast_scan_settings(project_id, preset_id, engine_configuration_id=1, post_scan_action_id=None,
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
        result = None
        relative_url = "/cxrestapi/sast/scanSettings"
        post_data = json.dumps(
            {
                "projectId": project_id,
                "presetId": preset_id,
                "engineConfigurationId": engine_configuration_id,
                "postScanActionId": post_scan_action_id,
                "emailNotifications": {
                    "failedScan": failed_scan_emails,
                    "beforeScan": before_scan_emails,
                    "afterScan": after_scan_emails,
                },
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxCreateScanSettingsResponse(
                scan_setting_response_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def update_sast_scan_settings(project_id, preset_id=1, engine_configuration_id=1, post_scan_action_id=None,
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
        result = None
        relative_url = "/cxrestapi/sast/scanSettings"
        put_data = json.dumps(
            {
                "projectId": project_id,
                "presetId": preset_id,
                "engineConfigurationId": engine_configuration_id,
                "postScanActionId": post_scan_action_id,
                "emailNotifications": {
                    "failedScan": failed_scan_emails,
                    "beforeScan": before_scan_emails,
                    "afterScan": after_scan_emails,
                },
            }
        )
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxCreateScanSettingsResponse(
                scan_setting_response_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def define_sast_scan_scheduling_settings(project_id, schedule_type, schedule_days, schedule_time,
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
        result = None
        relative_url = "/cxrestapi/sast/project/{projectId}/scheduling".format(projectId=project_id)
        put_data = json.dumps(
            {
                "scheduleType": schedule_type,
                "scheduledDays": list(schedule_days),
                "scheduleTime": schedule_time
            }
        )
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def assign_ticket_to_scan_results(results_id, ticket_id, api_version="1.0"):
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
        result = False
        relative_url = "/cxrestapi/sast/results/tickets"
        post_data = json.dumps(
            {
                "resultsId": [results_id],
                "ticketId": ticket_id
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def publish_last_scan_results_to_management_and_orchestration_by_project_id(project_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/sast/projects/{id}/publisher/policyFindings".format(id=project_id)
        response = post_request(relative_url=relative_url, data=None, headers=get_headers(api_version))
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxPolicyFindingResponse(
                policy_finding_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def get_the_publish_last_scan_results_to_management_and_orchestration_status(project_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/sast/projects/{id}/publisher/policyFindings/status".format(id=project_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxPolicyFindingsStatus(
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
        return result

    @staticmethod
    def get_short_vulnerability_description_for_a_scan_result(scan_id, path_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/results/{pathId}/shortDescription".format(id=scan_id, pathId=path_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json().get("shortDescription")
        return result

    @staticmethod
    def register_scan_report(scan_id, report_type, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/reports/sastScan"
        post_data = json.dumps(
            {
                "reportType": report_type,
                "scanId": scan_id
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            a_dict = response.json()
            result = CxRegisterScanReportResponse(
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
        return result

    @staticmethod
    def get_report_status_by_id(report_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/reports/sastScan/{id}/status".format(id=report_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxScanReportStatus(
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
        return result

    @staticmethod
    def get_report_by_id(report_id, api_version="1.0"):
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
        result = None
        relative_url = "/cxrestapi/reports/sastScan/{id}".format(id=report_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            # write r.content to file with "wb" mode
            result = response.content
        return result

    @staticmethod
    def is_scanning_finished(scan_id):
        """
        check if a scan is finished

        Args:
            scan_id (int): unique id of a scan

        Returns:
            boolean
        """
        is_finished = False

        scan_detail = ScansAPI.get_sast_scan_details_by_scan_id(scan_id=scan_id)
        if scan_detail.status.name == "Finished":
            is_finished = True

        return is_finished

    @staticmethod
    def is_report_generation_finished(report_id):
        """
        check if a report generation is finished

        Args:
            report_id (int): unique id of a report

        Returns:

        """
        is_finished = False

        report_status = ScansAPI.get_report_status_by_id(report_id)
        if report_status.status.value == "Created":
            is_finished = True

        return is_finished

    @staticmethod
    def get_scan_results_of_a_specific_query(scan_id, query_version_code, api_version="1.0"):
        """
        Get the scan results for a specific query in Attack Vector format. This format includes all nodes.

        Args:
            scan_id (int):
            query_version_code (int):
            api_version (str, optional):

        Returns:
            attack_vectors (`list` of `CxScanResultAttackVector`)
        """
        result = []
        relative_url = "/cxrestapi/sast/results/attack-vectors?scanId={scanId}&queryVersion={queryVersion}".format(
            scanId=scan_id, queryVersion=query_version_code
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            vectors = response.json().get('attackVectors')
            result = [
                construct_attack_vector(ac) for ac in vectors
            ]
        return result

    @staticmethod
    def get_scan_results_for_a_specific_query_group_by_best_fix_location(scan_id, query_version_code,
                                                                         api_version="1.0"):
        """

        Args:
            scan_id (int):
            query_version_code (int):
            api_version (str, optional):

        Returns:
           attack_vectors_by_bfl  (`list` of `CxScanResultAttackVectorByBFL`)
        """
        result = []
        relative_url = "/cxrestapi/sast/results/attack-vectors-by-bfl"
        relative_url += "?scanId={scanId}&queryVersion={queryVersion}".format(
            scanId=scan_id, queryVersion=query_version_code
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            attack_vectors_by_bfl = response.json().get("attackVectorsByBFL")
            result = [
                CxScanResultAttackVectorByBFL(
                    scan_id=ac_bfl.get("scanId"),
                    query_version_code=ac_bfl.get("queryVersion"),
                    best_fix_location_node=construct_scan_result_node(ac_bfl.get("bestFixLocationNode")),
                    attack_vectors=[construct_attack_vector(ac) for ac in ac_bfl.get("attackVectors")]
                ) for ac_bfl in attack_vectors_by_bfl
            ]
        return result

    @staticmethod
    def update_scan_result_labels_fields(scan_id, result_id, state, severity, user_assignment, comment,
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
            bool
        """
        result = False
        from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_version_number_as_int
        version = get_version_number_as_int()
        relative_url = "/cxrestapi/sast/scans/{scanId}/results/{resultId}".format(scanId=scan_id, resultId=result_id)
        if version >= 940:
            relative_url += "/labels"
        data = json.dumps({
            "state": state,
            "severity": severity,
            "userAssignment": user_assignment,
            "comment": comment,
        })
        response = patch_request(relative_url=relative_url, data=data, headers=get_headers(api_version))
        if response.status_code == OK:
            result = True
        return result

    @staticmethod
    def create_new_scan_with_settings(project_id, preset_id, zipped_source_file_path,
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
            CxCreateNewScanResponse
        """
        result = None
        relative_url = "/cxrestapi/sast/scanWithSettings"
        file_name = os.path.basename(zipped_source_file_path)
        if not exists(normpath(abspath(zipped_source_file_path))):
            print("zipped_source_file_path not exist: {}".format(zipped_source_file_path))
            return None
        m = MultipartEncoder(
            fields={
                "projectId": str(project_id),
                "overrideProjectSetting": str(override_project_setting),
                "isIncremental": str(is_incremental),
                "isPublic": str(is_public),
                "forceScan": str(force_scan),
                "comment": str(comment),
                "presetId": str(preset_id),
                "engineConfigurationId": str(engine_configuration_id),
                "zippedSource": (file_name, open(zipped_source_file_path, 'rb'), "application/zip"),
                "customFields": json.dumps(custom_fields),
                "postScanActionId": str(post_scan_action_id),
            }
        )
        headers = {"Content-Type": m.content_type}
        response = post_request(relative_url=relative_url, data=m, headers=get_headers(api_version, headers))
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxCreateNewScanResponse(
                scan_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def get_scan_result_labels_fields(scan_id, result_id, api_version="1.0"):
        """

        Args:
            scan_id (int): Unique Id of a scan
            result_id (int): Unique Id of the result path
            api_version (str, optional):

        Returns:
            CxScanResultLabelsFields
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{scanId}/results/{resultId}/labels".format(
            scanId=scan_id, resultId=result_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxScanResultLabelsFields(
                state=a_dict.get("state"),
                severity=a_dict.get("severity"),
                user_assignment=a_dict.get("userAssignment"),
                comment=a_dict.get("comment")
            )
        return result

    @staticmethod
    def get_scan_logs(scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            binary string, contains zip file content
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/logs".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.content
        return result

    @staticmethod
    def get_basic_metrics_of_a_scan(scan_id, api_version="3.0"):
        """
        https://checkmarx.atlassian.net/wiki/spaces/SAST/pages/3206498165/Configuring+and+Viewing+Scan+Metrics
        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanStatistics`
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/statistics".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxScanStatistics(
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
        return result

    @staticmethod
    def get_parsed_files_metrics_of_a_scan(scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanParsedFiles`
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/parsedFiles".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxScanParsedFiles(
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
        return result

    @staticmethod
    def get_failed_queries_metrics_of_a_scan(scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanFailedQueries`
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/failedQueries".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxScanFailedQueries(
                scan_id=item.get("id"),
                failed_queries=item.get("failedQueries")
            )
        return result

    @staticmethod
    def get_failed_general_queries_metrics_of_a_scan(scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanFailedGeneralQueries`
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/failedGeneralQueries".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxScanFailedGeneralQueries(
                scan_id=item.get("id"),
                failed_general_queries=item.get("failedGeneralQueries")
            )
        return result

    @staticmethod
    def get_succeeded_general_queries_metrics_of_a_scan(scan_id, api_version="3.0"):
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanSucceededGeneralQueries`
        """
        result = None
        relative_url = "/cxrestapi/sast/scans/{id}/succeededGeneralQueries".format(id=scan_id)
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxScanSucceededGeneralQueries(
                scan_id=item.get("id"),
                general_queries_result_count=item.get("generalQueriesResultCount")
            )
        return result
