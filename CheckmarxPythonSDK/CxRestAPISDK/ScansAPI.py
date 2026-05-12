from typing import List, Union
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
import os
import json
from os.path import normpath, exists, abspath

from CheckmarxPythonSDK.utilities.compat import OK, CREATED, NO_CONTENT, ACCEPTED
from .sast.projects.dto import CxLink, CxProject, CxPreset
from .sast.engines.dto import CxEngineServer, CxEngineConfiguration
from .sast.scans.dto import (
    CxScanState,
    CxPolicyFindingsStatus,
    CxResultsStatistics,
    CxPolicyFindingResponse,
    CxStatus,
    CxFinishedScanStatus,
    CxStatisticsResult,
    CxCreateNewScanResponse,
    CxRegisterScanReportResponse,
    CxScanType,
    CxScanDetail,
    CxScanReportStatus,
    CxDateAndTime,
    CxScanQueueDetail,
    CxScanStage,
    CxLanguageState,
    CxStatusDetail,
    CxScanSettings,
    CxCreateScanSettingsResponse,
    CxEmailNotification,
    CxLanguage,
    CxScanResultAttackVectorByBFL,
    CxScanResultLabelsFields,
    CxScanStatistics,
    CxScanFileCountOfLanguage,
    CxLanguageStatistic,
    CxScanParsedFiles,
    CxScanParsedFilesMetric,
    CxScanFailedQueries,
    CxScanFailedGeneralQueries,
    CxScanSucceededGeneralQueries,
    CxPostScanActionConditions,
    CxScanResultAttackVector,
    CxScanResultsPage,
)


class ScansAPI(object):
    """
    scans API
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = api_client.configuration.server_base_url.rstrip("/")

    def get_all_scans_for_project(
        self,
        project_id: int = None,
        scan_status: str = None,
        last: int = None,
        api_version: str = "1.0",
    ) -> List[CxScanDetail]:
        """
        Get details of all SAST scans for a specific project.


        Args:
            project_id (int, optional): Unique Id of the project
            scan_status (str, optional): The current status of the scan, only support the following
                        ["Scanning", "Finished", "Canceled", "Failed"]
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
        url = f"{self.base_url}/cxrestapi/sast/scans"
        optionals = []
        if project_id:
            optionals.append("projectId={}".format(project_id))
        if scan_status:
            if scan_status not in ["Scanning", "Finished", "Canceled", "Failed"]:
                raise ValueError(
                    "scanStatus can only be Scanning, Finished, Canceled, Failed"
                )
            optionals.append("scanStatus={}".format(scan_status))
        if last:
            optionals.append("last={}".format(last))
        if optionals:
            url += "?" + "&".join(optionals)

        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxScanDetail.from_dict(item) for item in response.json()]
        return result

    def get_last_scan_id_of_a_project(
        self,
        project_id: int,
        only_finished_scans: bool = False,
        only_completed_scans: bool = True,
        only_real_scans: bool = True,
        only_full_scans: bool = True,
        only_public_scans: bool = True,
    ) -> Union[int, None]:
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

        all_scans_for_this_project = self.get_all_scans_for_project(project_id)

        if only_finished_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.status.name == "Finished", all_scans_for_this_project
            )
        if only_completed_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.finished_scan_status.value in ("Completed", None),
                all_scans_for_this_project,
            )

        if only_real_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.date_and_time.started_on
                != scan.date_and_time.finished_on,
                all_scans_for_this_project,
            )

        if only_full_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.is_incremental is False, all_scans_for_this_project
            )

        if only_public_scans:
            all_scans_for_this_project = filter(
                lambda scan: scan.is_public is True, all_scans_for_this_project
            )

        all_scans_for_this_project = sorted(
            all_scans_for_this_project, key=lambda scan: scan.id, reverse=True
        )
        if len(all_scans_for_this_project) > 0:
            scan_id = all_scans_for_this_project[0].id

        return scan_id

    def create_new_scan(
        self,
        project_id: int,
        is_incremental: bool = False,
        is_public: bool = True,
        force_scan: bool = True,
        comment: str = "",
        custom_fields: dict = None,
        api_version: str = "5.0",
    ) -> CxCreateNewScanResponse:
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
        url = f"{self.base_url}/cxrestapi/sast/scans"
        post_data = json.dumps(
            {
                "projectId": project_id,
                "isIncremental": is_incremental,
                "isPublic": is_public,
                "forceScan": force_scan,
                "comment": comment,
                "customFields": custom_fields,
            }
        )
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers=get_headers(api_version)
        )
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxCreateNewScanResponse.from_dict(a_dict)
        return result

    def get_sast_scan_details_by_scan_id(
        self, scan_id: int, api_version: str = "5.0"
    ) -> CxScanDetail:
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
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            item = response.json()
            result = CxScanDetail.from_dict(item)
        return result

    def add_or_update_a_comment_by_scan_id(
        self, scan_id: int, comment: str, api_version: str = "1.0"
    ) -> bool:
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
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}"
        patch_data = json.dumps({"comment": comment})
        response = self.api_client.call_api(
            "PATCH", url, data=patch_data, headers=get_headers(api_version)
        )
        return response.status_code == NO_CONTENT

    def delete_scan_by_scan_id(self, scan_id: int, api_version: str = "1.0") -> bool:
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
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}"
        response = self.api_client.call_api(
            "DELETE", url, headers=get_headers(api_version)
        )
        return response.status_code == ACCEPTED

    def get_statistics_results_by_scan_id(
        self, scan_id: int, api_version: str = "6.0"
    ) -> CxStatisticsResult:
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
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/resultsStatistics"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxStatisticsResult.from_dict(response.json())
        return result

    def get_scan_queue_details_by_scan_id(
        self, scan_id: int, api_version: str = "1.0"
    ) -> CxScanQueueDetail:
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
        url = f"{self.base_url}/cxrestapi/sast/scansQueue/{scan_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            item = response.json()
            result = CxScanQueueDetail.from_dict(item)
        return result

    def update_queued_scan_status_by_scan_id(
        self, scan_id: int, api_version: str = "1.2"
    ) -> bool:
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
        url = f"{self.base_url}/cxrestapi/sast/scansQueue/{scan_id}"
        patch_data = json.dumps({"status": "Canceled"})
        response = self.api_client.call_api(
            "PATCH", url, data=patch_data, headers=get_headers(api_version)
        )
        return response.status_code == OK

    def cancel_scan(self, scan_id: int, api_version: str = "1.2"):
        return self.update_queued_scan_status_by_scan_id(
            scan_id=scan_id, api_version=api_version
        )

    def get_all_scan_details_in_queue(
        self, project_id: int = None, api_version: str = "1.0"
    ) -> List[CxScanQueueDetail]:
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
        url = f"{self.base_url}/cxrestapi/sast/scansQueue"
        if project_id:
            url += "?projectId=" + str(project_id)
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxScanQueueDetail.from_dict(item) for item in response.json()]
        return result

    def get_scan_settings_by_project_id(
        self, project_id: int, api_version: str = "4.0"
    ) -> CxScanSettings:
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
        url = f"{self.base_url}/cxrestapi/sast/scanSettings/{project_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxScanSettings.from_dict(response.json())
        return result

    def define_sast_scan_settings(
        self,
        project_id: int,
        preset_id: int,
        engine_configuration_id: int = 1,
        post_scan_action_id: int = None,
        failed_scan_emails: List[str] = None,
        before_scan_emails: List[str] = None,
        after_scan_emails: List[str] = None,
        run_only_when_new_results: bool = True,
        run_only_when_new_results_min_severity: int = 0,
        post_scan_action_arguments: str = None,
        api_version: str = "4.0",
    ) -> CxCreateScanSettingsResponse:
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
            run_only_when_new_results (bool):
            run_only_when_new_results_min_severity (int):
            post_scan_action_arguments (str):
            api_version (str, optional):

        Returns:
            :obj:`CxCreateScanSettingsResponse`

        Raises：
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        if failed_scan_emails and not isinstance(failed_scan_emails, list):
            raise ValueError("failed_scan_emails should be a list")
        if before_scan_emails and not isinstance(before_scan_emails, list):
            raise ValueError("before_scan_emails should be a list")
        if after_scan_emails and not isinstance(after_scan_emails, list):
            raise ValueError("after_scan_emails should be a list")
        url = f"{self.base_url}/cxrestapi/sast/scanSettings"
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
                "postScanActionConditions": {
                    "runOnlyWhenNewResults": run_only_when_new_results,
                    "runOnlyWhenNewResultsMinSeverity": run_only_when_new_results_min_severity,
                },
                "postScanActionArguments": post_scan_action_arguments,
            }
        )
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            a_dict = response.json()
            result = CxCreateScanSettingsResponse.from_dict(a_dict)
        return result

    def update_sast_scan_settings(
        self,
        project_id: int,
        preset_id: int = 1,
        engine_configuration_id: int = 1,
        post_scan_action_id: int = None,
        failed_scan_emails: List[str] = None,
        before_scan_emails: List[str] = None,
        after_scan_emails: List[str] = None,
        run_only_when_new_results: bool = True,
        run_only_when_new_results_min_severity: int = 0,
        post_scan_action_arguments: str = None,
        api_version: str = "4.0",
    ) -> CxCreateScanSettingsResponse:
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
            run_only_when_new_results (bool):
            run_only_when_new_results_min_severity (int):
            post_scan_action_arguments (str):
            api_version (str, optional):

        Returns:
            :obj:`CxCreateScanSettingsResponse`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scanSettings"
        if failed_scan_emails and not isinstance(failed_scan_emails, list):
            raise ValueError("failed_scan_emails should be a list")
        if before_scan_emails and not isinstance(before_scan_emails, list):
            raise ValueError("before_scan_emails should be a list")
        if after_scan_emails and not isinstance(after_scan_emails, list):
            raise ValueError("after_scan_emails should be a list")
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
                "postScanActionConditions": {
                    "runOnlyWhenNewResults": run_only_when_new_results,
                    "runOnlyWhenNewResultsMinSeverity": run_only_when_new_results_min_severity,
                },
                "postScanActionArguments": post_scan_action_arguments,
            }
        )
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            a_dict = response.json()
            result = CxCreateScanSettingsResponse.from_dict(a_dict)
        return result

    def define_sast_scan_scheduling_settings(
        self,
        project_id: int,
        schedule_type: str,
        schedule_days: List[str],
        schedule_time: str,
        api_version: str = "1.0",
    ) -> bool:
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
        url = f"{self.base_url}/cxrestapi/sast/project/{project_id}/scheduling"
        put_data = json.dumps(
            {
                "scheduleType": schedule_type,
                "scheduledDays": list(schedule_days),
                "scheduleTime": schedule_time,
            }
        )
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers=get_headers(api_version)
        )
        return response.status_code == NO_CONTENT

    def assign_ticket_to_scan_results(
        self, results_id: str, ticket_id: str, api_version: str = "1.0"
    ) -> bool:
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
        url = f"{self.base_url}/cxrestapi/sast/results/tickets"
        post_data = json.dumps({"resultsId": [results_id], "ticketId": ticket_id})
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers=get_headers(api_version)
        )
        return response.status_code == NO_CONTENT

    def publish_last_scan_results_to_management_and_orchestration_by_project_id(
        self, project_id: int, api_version: str = "1.0"
    ) -> CxPolicyFindingResponse:
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
        url = f"{self.base_url}/cxrestapi/sast/projects/{project_id}/publisher/policyFindings"
        response = self.api_client.call_api(
            "POST", url, data=None, headers=get_headers(api_version)
        )
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxPolicyFindingResponse.from_dict(a_dict)
        return result

    def get_the_publish_last_scan_results_to_management_and_orchestration_status(
        self, project_id: int, api_version: str = "1.0"
    ) -> CxPolicyFindingsStatus:
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
        url = f"{self.base_url}/cxrestapi/sast/projects/{project_id}/publisher/policyFindings/status"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            a_dict = response.json()
            result = CxPolicyFindingsStatus.from_dict(a_dict)
        return result

    def get_short_vulnerability_description_for_a_scan_result(
        self, scan_id: int, path_id: int, api_version: str = "1.0"
    ) -> str:
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
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/results/{path_id}/shortDescription"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.json().get("shortDescription")
        return result

    def register_scan_report(
        self, scan_id: int, report_type: str, api_version: str = "1.0"
    ) -> CxRegisterScanReportResponse:
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
        url = f"{self.base_url}/cxrestapi/reports/sastScan"
        post_data = json.dumps({"reportType": report_type, "scanId": scan_id})
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers=get_headers(api_version)
        )
        if response.status_code == ACCEPTED:
            result = CxRegisterScanReportResponse.from_dict(response.json())
        return result

    def get_report_status_by_id(
        self, report_id: int, api_version: str = "1.0"
    ) -> CxScanReportStatus:
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
        url = f"{self.base_url}/cxrestapi/reports/sastScan/{report_id}/status"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            a_dict = response.json()
            result = CxScanReportStatus.from_dict(a_dict)
        return result

    def get_report_by_id(self, report_id: int, api_version: str = "1.0") -> bytes:
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
        url = f"{self.base_url}/cxrestapi/reports/sastScan/{report_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            # write r.content to file with "wb" mode
            result = response.content
        return result

    def is_scanning_finished(self, scan_id: int) -> bool:
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

    def is_report_generation_finished(self, report_id: int) -> bool:
        """
        check if a report generation is finished

        Args:
            report_id (int): unique id of a report

        Returns:

        """
        report_status = self.get_report_status_by_id(report_id)
        return report_status.status.value == "Created"

    def get_scan_results_of_a_specific_query(
        self, scan_id: int, query_version_code: int, api_version: str = "1.0"
    ) -> List[CxScanResultAttackVector]:
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
        url = f"{self.base_url}/cxrestapi/sast/results/attack-vectors?scanId={scan_id}&queryVersion={query_version_code}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            vectors = response.json().get("attackVectors")
            result = [CxScanResultAttackVector.from_dict(ac) for ac in vectors]
        return result

    def get_scan_results_for_a_specific_query_group_by_best_fix_location(
        self, scan_id: int, query_version_code: int, api_version: str = "1.0"
    ) -> List[CxScanResultAttackVectorByBFL]:
        """

        Args:
            scan_id (int):
            query_version_code (int):
            api_version (str, optional):

        Returns:
           attack_vectors_by_bfl  (`list` of `CxScanResultAttackVectorByBFL`)
        """
        result = []
        url = f"{self.base_url}/cxrestapi/sast/results/attack-vectors-by-bfl"
        url += "?scanId={scanId}&queryVersion={queryVersion}".format(
            scanId=scan_id, queryVersion=query_version_code
        )
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            attack_vectors_by_bfl = response.json().get("attackVectorsByBFL")
            result = [
                CxScanResultAttackVectorByBFL.from_dict(ac_bfl)
                for ac_bfl in attack_vectors_by_bfl
            ]
        return result

    def update_scan_result_labels_fields(
        self,
        scan_id: int,
        result_id: int,
        state: int,
        severity: int,
        user_assignment: str,
        comment: str,
        api_version: str = "1.0",
    ) -> bool:
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
        from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_version_number_as_int

        version = get_version_number_as_int()
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/results/{result_id}"
        if version >= 940:
            url += "/labels"
        data = json.dumps(
            {
                "state": state,
                "severity": severity,
                "userAssignment": user_assignment,
                "comment": comment,
            }
        )
        response = self.api_client.call_api(
            "PATCH", url, data=data, headers=get_headers(api_version)
        )
        return response.status_code == OK

    def create_new_scan_with_settings(
        self,
        project_id: int,
        comment: str,
        preset_id: int,
        zipped_source_file_path: str,
        override_project_setting: bool = False,
        is_incremental: bool = False,
        is_public: bool = True,
        force_scan: bool = True,
        engine_configuration_id: int = 0,
        custom_fields: dict = None,
        post_scan_action_id: int = None,
        run_post_scan_only_when_new_results: bool = False,
        run_post_scan_min_severity: int = None,
        post_scan_action_arguments: str = None,
        api_version: str = "5.0",
    ) -> Union[CxCreateNewScanResponse, None]:
        """

        Args:
            project_id (int): Specifies the Unique Id of the specific project to be scanned
            comment (str): Specifies the scan comment
            preset_id (int): Specify the preset id to use during the scan, 0 = use project's default
            override_project_setting (bool): Specifies whether to overwrite project settings to be the default for the
                                            next scans .If set to false or empty - do not overwrite project settings.
                                            If set to true - overwrite project settings
            zipped_source_file_path (str):
            is_incremental (bool):  Specifies whether the scan is incremental of full
            is_public (bool): Specifies whether the requested scan is public or private
            force_scan (bool): Specifies whether the code should be scanned regardless of unchanged code
            engine_configuration_id (int): Specify the engine-configuration to use during the scan, 0 = use project's
                                            default
            custom_fields (dict, optional): Any custom fields used to tag the scan.
                                                Example: {"key1":"val1","key2":"val2"}
            post_scan_action_id (int, optional): Specify post action to be executed after scan is completed
            run_post_scan_only_when_new_results(bool, optional): Specify if the configured post scan action will be
                                    executed only if new results are found, compared to the previous scan.
                                    Used in conjunction with PostScanActionId.
            run_post_scan_min_severity(int, optional): Specify the minimal severity value when evaluating new results
                                        compared to the previous scan. Used in conjunction with
                                        RunPostScanOnlyWhenNewResults.
            post_scan_action_arguments(str, optional): Specify the additional arguments to add to the post scan action.
                                    Used in conjunction with PostScanActionId.
            api_version (str, optional):

        Returns:
            CxCreateNewScanResponse
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scanWithSettings"
        file_name = os.path.basename(zipped_source_file_path)
        if not exists(normpath(abspath(zipped_source_file_path))):
            print(
                "zipped_source_file_path not exist: {}".format(zipped_source_file_path)
            )
            return None
        fields = {
            "projectId": str(project_id),
            "overrideProjectSetting": str(override_project_setting),
            "isIncremental": str(is_incremental),
            "isPublic": str(is_public),
            "forceScan": str(force_scan),
            "presetId": str(preset_id),
            "engineConfigurationId": str(engine_configuration_id),
            "zippedSource": (
                file_name,
                open(zipped_source_file_path, "rb"),
                "application/zip",
            ),
        }
        if comment:
            fields.update({"comment": str(comment)})
        if custom_fields:
            fields.update(
                {
                    "customFields": json.dumps(custom_fields),
                }
            )
        if post_scan_action_id:
            fields.update(
                {
                    "postScanActionId": str(post_scan_action_id),
                    "postScanActionArguments": str(post_scan_action_arguments),
                }
            )
            fields.update(
                {
                    "runPostScanOnlyWhenNewResults": run_post_scan_only_when_new_results,
                    "runPostScanMinSeverity": run_post_scan_min_severity,
                }
            )
            if run_post_scan_only_when_new_results:
                pass
        files = {k: v for k, v in fields.items() if isinstance(v, tuple)}
        data = {k: v for k, v in fields.items() if not isinstance(v, tuple)}
        response = self.api_client.call_api(
            "POST", url, files=files, data=data, headers=get_headers(api_version)
        )
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxCreateNewScanResponse.from_dict(a_dict)
        return result

    def get_scan_result_labels_fields(
        self, scan_id: int, result_id: int, api_version: str = "1.0"
    ) -> CxScanResultLabelsFields:
        """

        Args:
            scan_id (int): Unique Id of a scan
            result_id (int): Unique Id of the result path
            api_version (str, optional):

        Returns:
            CxScanResultLabelsFields
        """
        result = None
        url = (
            f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/results/{result_id}/labels"
        )
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxScanResultLabelsFields.from_dict(response.json())
        return result

    def get_scan_logs(self, scan_id: int, api_version: str = "5.0") -> bytes:
        """
        Gets Scan logs.
        Args:
            scan_id (int):
            api_version (str):

        Returns:
            binary string, contains zip file content
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/logs"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.content
        return result

    def get_basic_metrics_of_a_scan(
        self, scan_id: int, api_version: str = "5.0"
    ) -> CxScanStatistics:
        """
        https://checkmarx.atlassian.net/wiki/spaces/SAST/pages/3206498165/Configuring+and+Viewing+Scan+Metrics
        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanStatistics`
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/statistics"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxScanStatistics.from_dict(response.json())
        return result

    def get_parsed_files_metrics_of_a_scan(
        self, scan_id: int, api_version: str = "3.0"
    ) -> CxScanParsedFiles:
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanParsedFiles`
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/parsedFiles"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            item = response.json()
            result = CxScanParsedFiles.from_dict(item)
        return result

    def get_failed_queries_metrics_of_a_scan(
        self, scan_id: int, api_version: str = "3.0"
    ) -> CxScanFailedQueries:
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanFailedQueries`
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/failedQueries"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            item = response.json()
            result = CxScanFailedQueries.from_dict(item)
        return result

    def get_failed_general_queries_metrics_of_a_scan(
        self, scan_id: int, api_version: str = "3.0"
    ) -> CxScanFailedGeneralQueries:
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanFailedGeneralQueries`
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/failedGeneralQueries"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            item = response.json()
            result = CxScanFailedGeneralQueries.from_dict(item)
        return result

    def get_succeeded_general_queries_metrics_of_a_scan(
        self, scan_id: int, api_version: str = "3.0"
    ) -> CxScanSucceededGeneralQueries:
        """

        Args:
            scan_id (int):
            api_version (str):

        Returns:
            `CxScanSucceededGeneralQueries`
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/succeededGeneralQueries"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            item = response.json()
            result = CxScanSucceededGeneralQueries.from_dict(item)
        return result

    def get_result_path_comments_history(
        self,
        scan_id: int,
        path_id: int,
        comment_to_display: str = "All",
        api_version: str = "4.0",
    ) -> dict:
        """

        Args:
            scan_id (int):
            path_id (int):
            comment_to_display (str): All, Latest
            api_version (str):

        Returns:
            dict
            example:
                {'comments': ['happy yang jvl_git, [2023年12月28日 15:01]: Changed status to Confirmed ']}
        """
        result = None

        if comment_to_display not in ["All", "Latest"]:
            raise ValueError(
                "parameter comment_to_display accepted value are All, Latest."
            )

        url = f"{self.base_url}/cxrestapi/sast/resultPathCommentsHistory?id={scan_id}&pathId={path_id}&commentToDisplay={comment_to_display}"

        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.json()
        return result

    def lock_scan(self, scan_id: int, api_version: str = "4.0") -> bool:
        """

        Args:
            scan_id (int): Unique ID of a specific scan
            api_version (str):

        Returns:

        """
        url = f"{self.base_url}/cxrestapi/sast/lockScan?id={scan_id}"
        response = self.api_client.call_api(
            "PUT", url, data=None, headers=get_headers(api_version)
        )
        return response.status_code == OK

    def unlock_scan(self, scan_id: int, api_version: str = "4.0") -> bool:
        """

        Args:
            scan_id (int): Unique ID of a specific scan
            api_version (str):

        Returns:

        """
        url = f"{self.base_url}/cxrestapi/sast/unLockScan?id={scan_id}"
        response = self.api_client.call_api(
            "PUT", url, data=None, headers=get_headers(api_version)
        )
        return response.status_code == OK

    def get_scan_result_labels_action_fields(
        self, scan_id: int, path_id: int, api_version: str = "5.0"
    ) -> List[dict]:
        """
        Get scan result labels action fields
        Args:
            scan_id (int):
            path_id (int):
            api_version (str):

        Returns:
            Labels are changes made on the results' properties by the user.
            list of dict
            example:
            [
              {
                "user": "tod-cyber",
                "comment": "Changed status to Urgent",
                "createdDate": "2024-07-14T20:05:45.7517605"
              },
              {
                "user": "jim-developer",
                "comment": "Changed severity to Medium",
                "createdDate": "2024-07-14T20:05:45.7517605"
              }
            ]
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{scan_id}/actionResults/{path_id}/labels"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.json()
        return result

    def get_compare_results_of_two_scans(
        self, old_scan_id: int, new_scan_id: int, api_version: str = "5.1"
    ) -> List[dict]:
        """

        Args:
            old_scan_id (int):
            new_scan_id (int):
            api_version (str):

        Returns:
            list of dict
            example:
            [
                {
                  'similarityID': 994470032,
                  'queryId': 589,
                  'pathId': 21,
                  'sourceFolder': 'java\\org\\cysecurity\\cspf\\jvl\\controller',
                  'sourceFile': 'Install.java',
                  'sourceLine': 54,
                  'sourceObject': '""dburl""',
                  'destFolder': 'java\\org\\cysecurity\\cspf\\jvl\\controller',
                  'destFile': 'Install.java',
                  'destLine': 112,
                  'numberOfNodes': 0,
                  'destObject': 'dburl',
                  'comment': 'happy yang jvl_git, [2023年10月13日 14:31]: Explain why it is not exploitable. ÿ',
                  'state': 1,
                  'severity': 3,
                  'assignedUser': '',
                  'resultStatus': 0,
                  'queryVersionCode': 0,
                  'scanId': 1000076,
                  'comparedToScanId': 1000118,
                  'comparedToScanPathId': -1,
                  'queryName': 'Connection_String_Injection'
                }
            ]

        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{old_scan_id}/compareResultsTo/{new_scan_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.json()
            result = result.get("results")
        return result

    def get_compare_results_summary_of_two_scans(
        self, old_scan_id: int, new_scan_id: int, api_version: str = "5.0"
    ) -> dict:
        """

        Args:
            old_scan_id (int):
            new_scan_id (int):
            api_version (str):

        Returns:
            dict
            example:
                {
                  'high': {'fixed': 100, 'new': 0, 'reOccured': 12},
                  'info': {'fixed': 0, 'new': 0, 'reOccured': 0},
                  'low': {'fixed': 233, 'new': 36, 'reOccured': 0},
                  'medium': {'fixed': 117, 'new': 6, 'reOccured': 46},
                  'total': {'fixed': 450, 'new': 42, 'reOccured': 58}
                }
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/scans/{old_scan_id}/compareSummaryTo/{new_scan_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.json()
        return result

    def get_a_collection_of_scans_by_project(
        self,
        last: int = None,
        project_id: int = None,
        scan_status: str = None,
        api_version: str = "5.0",
    ) -> dict:
        """

        Args:
            last (int): Amount of the latest scans
            project_id (int): Unique ID of a specific project
            scan_status (str, optional): Specifies the scan stage: ["Scanning", "Finished", "Canceled", "Failed"]
            api_version (str):

        Returns:

        """
        result = None
        if scan_status and scan_status not in [
            "Scanning",
            "Finished",
            "Canceled",
            "Failed",
        ]:
            raise ValueError(
                'parameter scan_status should be a member from list ["Scanning", "Finished", '
                '"Canceled", "Failed"]'
            )
        url = f"{self.base_url}/cxrestapi/sast/scans"
        optional = []
        if last:
            optional.append("last={last}".format(last=last))
        if project_id:
            optional.append("projectId={projectId}".format(projectId=project_id))
        if scan_status:
            if not last or not project_id:
                raise ValueError(
                    "Both last and project_id can not be None when scan_status is not None"
                )
            optional.append("&scanStatus={scanStatus}".format(scanStatus=scan_status))
        if optional:
            url += "?" + "&".join(optional)
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = response.json()
        return result

    def get_scan_results_in_paged_mode(self, scan_id, offset, limit, lcid=None):
        """
        Args:
            scan_id (int): Unique ID of a scan
            offset  (int): Page offset
            limit   (int): Page size
            lcid    (int): Language Id

        Returns:
            :obj:CxScnResultsResponse

        Raises:
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/results?scanId={scan_id}&offset={offset}&limit={limit}"
        if lcid is not None:
            url = url + f"&LCID={lcid}"
        response = self.api_client.call_api("GET", url)
        if response.status_code == OK:
            data = response.json()
            result = CxScanResultsPage.from_dict(data)

        return result
