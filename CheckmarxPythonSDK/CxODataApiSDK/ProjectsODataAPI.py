from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxODataApiSDK.config import construct_configuration
from ..CxPortalSoapApiSDK import get_version_number_as_int


class ProjectsODataAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_top_n_projects_by_risk_score(self, number_of_projects: int) -> List[dict]:
        """
        Requested result: list the 5 Projects whose most recent scans yielded the highest Risk Score
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan/RiskScore%20desc&$top=5

        Args:
            number_of_projects (int):

        Returns:
            `list` of `dict`
            sample
            [
             {
             'Id': 5, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
             'CreatedDate': '2020-11-01T15:14:27.907Z', 'OwnerId': 2,
             'OwningTeamId': '00000000-1111-1111-b111-989c9070eb11',
              'EngineConfigurationId': 1, 'IssueTrackingSettings': None,
              'SourcePath': '', 'SourceProviderCredentials': '',
              'ExcludedFiles': '', 'ExcludedFolders': '', 'OriginClientTypeId': 0, 'PresetId': 36,
              'LastScanId': 1000005, 'TotalProjectScanCount': 1, 'SchedulingExpression': None,
              'LastScan': {
                'Id': 1000017, 'SourceId': '0000000070_001607655511_0-1553425091',
                'Comment': 'Attempt to perform scan on 11/16/2020 3:05:03 PM - No code changes were detected; ',
                'IsIncremental': False, 'ScanType': 1, 'Origin': 'Visual-Studio-Code', 'OwnerId': None,
                'OwningTeamId': 1, 'InitiatorName': 'happy yang', 'ProjectName': 'jvl_local',
                'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer', 'Path': ' N/A (Zip File)',
                'FileCount': 70, 'LOC': 6907, 'FailedLOC': 282, 'ProductVersion': '9.2.0.41015 HF6',
                'IsForcedScan': False, 'ScanRequestedOn': '2020-11-16T15:05:03.157+08:00',
                'QueuedOn': '2020-11-16T15:05:03.157+08:00', 'EngineStartedOn': '2020-11-16T15:05:03.157+08:00',
                'EngineFinishedOn': None, 'ScanCompletedOn': '2020-11-16T15:05:03.157+08:00',
                'ScanDuration': '1900-01-01T00:00:00+08:00', 'ProjectId': 10, 'EngineServerId': 1, 'PresetId': 36,
                'QueryLanguageVersionId': 3, 'ScannedLanguageIds': 1073741834, 'TotalVulnerabilities': 850,
                'High': 271, 'Medium': 179, 'Low': 392, 'Info': 8, 'RiskScore': 100, 'QuantityLevel': 100,
                'StatisticsUpdateDate': '2020-11-16T15:05:04.223+08:00', 'StatisticsUpToDate': 1,
                'IsPublic': True, 'IsLocked': False
                }
              },
            ]
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects"
        relative_url += "?$expand=LastScan&$orderby=LastScan/RiskScore%20desc&$top={n}".format(n=number_of_projects)
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_top_n_projects_by_last_scan_duration(self, number_of_projects: int) -> List[dict]:
        """
        Requested result: list the 5 Projects whose most recent scan had the longest duration
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan/ScanDuration%20desc&$top=5

        Args:
            number_of_projects (int):

        Returns:
             `list` of `dict`

             example:

             [{'Id': 10, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
             'CreatedDate': '2020-11-02T04:48:19.783+08:00', 'OwnerId': None, 'OwningTeamId': 1,
             'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
             'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '',
             'OriginClientTypeId': 0, 'PresetId': 36, 'LastScanId': 1000017, 'TotalProjectScanCount': 4,
             'SchedulingExpression': None,
             'LastScan': {'
                 Id': 1000017, 'SourceId': '0000000070_001607655511_0-1553425091',
                 'Comment': 'Attempt to perform scan on 11/16/2020 3:05:03 PM - No code changes were detected; ',
                 'IsIncremental': False, 'ScanType': 1, 'Origin': 'Visual-Studio-Code', 'OwnerId': None,
                 'OwningTeamId': 1, 'InitiatorName': 'happy yang', 'ProjectName': 'jvl_local',
                 'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer', 'Path': ' N/A (Zip File)',
                 'FileCount': 70, 'LOC': 6907, 'FailedLOC': 282, 'ProductVersion': '9.2.0.41015 HF6',
                 'IsForcedScan': False, 'ScanRequestedOn': '2020-11-16T15:05:03.157+08:00',
                 'QueuedOn': '2020-11-16T15:05:03.157+08:00', 'EngineStartedOn': '2020-11-16T15:05:03.157+08:00',
                 'EngineFinishedOn': None, 'ScanCompletedOn': '2020-11-16T15:05:03.157+08:00',
                 'ScanDuration': '1900-01-01T00:00:00+08:00', 'ProjectId': 10, 'EngineServerId': 1,
                 'PresetId': 36, 'QueryLanguageVersionId': 3, 'ScannedLanguageIds': 1073741834,
                 'TotalVulnerabilities': 850, 'High': 271, 'Medium': 179, 'Low': 392, 'Info': 8, 'RiskScore': 100,
                 'QuantityLevel': 100, 'StatisticsUpdateDate': '2020-11-16T15:05:04.223+08:00', 'StatisticsUpToDate': 1,
                 'IsPublic': True, 'IsLocked': False
             }
             }]
        """

        relative_url = "/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan"
        relative_url += "/ScanDuration%20desc&$top={n}".format(n=number_of_projects)

        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_all_projects_with_their_last_scan_and_the_high_vulnerabilities(self):
        """
        Requested result: list all projects, and for each project list the security issues (vulnerabilities) with
        a High severity degree found in the project's most recent scan.
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan
        ($expand=Results($filter=Severity%20eq%20CxDataRepository.Severity%27High%27))

        Returns:
            `list` of `dict`

            example:
            [{
            'Id': 10, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
            'CreatedDate': '2020-11-02T04:48:19.783+08:00', 'OwnerId': None, 'OwningTeamId': 1,
            'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
            'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '',
            'OriginClientTypeId': 0, 'PresetId': 36, 'LastScanId': 1000017, 'TotalProjectScanCount': 4,
            'SchedulingExpression': None,
            'LastScan': {
                'Id': 1000017, 'SourceId': '0000000070_001607655511_0-1553425091',
                'Comment': 'Attempt to perform scan on 11/16/2020 3:05:03 PM - No code changes were detected; ',
                'IsIncremental': False, 'ScanType': 1, 'Origin': 'Visual-Studio-Code', 'OwnerId': None,
                'OwningTeamId': 1, 'InitiatorName': 'happy yang', 'ProjectName': 'jvl_local',
                'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer', 'Path': ' N/A (Zip File)',
                'FileCount': 70, 'LOC': 6907, 'FailedLOC': 282, 'ProductVersion': '9.2.0.41015 HF6',
                'IsForcedScan': False, 'ScanRequestedOn': '2020-11-16T15:05:03.157+08:00',
                'QueuedOn': '2020-11-16T15:05:03.157+08:00', 'EngineStartedOn': '2020-11-16T15:05:03.157+08:00',
                'EngineFinishedOn': None, 'ScanCompletedOn': '2020-11-16T15:05:03.157+08:00',
                'ScanDuration': '1900-01-01T00:00:00+08:00', 'ProjectId': 10, 'EngineServerId': 1,
                'PresetId': 36, 'QueryLanguageVersionId': 3, 'ScannedLanguageIds': 1073741834,
                'TotalVulnerabilities': 850, 'High': 271, 'Medium': 179, 'Low': 392, 'Info': 8, 'RiskScore': 100,
                'QuantityLevel': 100, 'StatisticsUpdateDate': '2020-11-16T15:05:04.223+08:00', 'StatisticsUpToDate': 1,
                 'IsPublic': True, 'IsLocked': False,
                 'Results': [
                    {'Id': 16, 'ResultId': '1000017-16', 'ScanId': 1000017, 'SimilarityId': 646035161,
                    'RawPriority': None, 'PathId': 16, 'ConfidenceLevel': 0, 'Date': '2020-11-16T15:05:03.273+08:00',
                    'Severity': 'High', 'StateId': 0, 'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None,
                    'QueryId': 589, 'QueryVersionId': 56089346}, {'Id': 17, 'ResultId': '1000017-17', 'ScanId': 1000017,
                     'SimilarityId': -750088295, 'RawPriority': None, 'PathId': 17, 'ConfidenceLevel': 0,
                     'Date': '2020-11-16T15:05:03.277+08:00', 'Severity': 'High', 'StateId': 0,
                     'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None, 'QueryId': 589,
                     'QueryVersionId': 56089346},]
            }]
        """
        relative_url = ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results($filter="
                        "Severity%20eq%20CxDataRepository.Severity%27High%27))")

        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_projects_that_have_high_vulnerabilities_in_the_last_scan(self) -> List[dict]:
        """
        Requested result:list only projects that had vulnerabilities with a High severity degree found
        in their last scan
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results)&
        $filter=LastScan/Results/any(r:%20r/Severity%20eq%20CxDataRepository.Severity%27High%27)

        Returns:
            [{
            'Id': 10, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
            'CreatedDate': '2020-11-02T04:48:19.783+08:00', 'OwnerId': None, 'OwningTeamId': 1,
            'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
            'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '',
            'OriginClientTypeId': 0, 'PresetId': 36, 'LastScanId': 1000017, 'TotalProjectScanCount': 4,
            'SchedulingExpression': None,
            'LastScan': {
                'Id': 1000017, 'SourceId': '0000000070_001607655511_0-1553425091',
                'Comment': 'Attempt to perform scan on 11/16/2020 3:05:03 PM - No code changes were detected; ',
                'IsIncremental': False, 'ScanType': 1, 'Origin': 'Visual-Studio-Code', 'OwnerId': None,
                'OwningTeamId': 1, 'InitiatorName': 'happy yang', 'ProjectName': 'jvl_local',
                'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer', 'Path': ' N/A (Zip File)',
                'FileCount': 70, 'LOC': 6907, 'FailedLOC': 282, 'ProductVersion': '9.2.0.41015 HF6',
                'IsForcedScan': False, 'ScanRequestedOn': '2020-11-16T15:05:03.157+08:00',
                'QueuedOn': '2020-11-16T15:05:03.157+08:00', 'EngineStartedOn': '2020-11-16T15:05:03.157+08:00',
                'EngineFinishedOn': None, 'ScanCompletedOn': '2020-11-16T15:05:03.157+08:00',
                'ScanDuration': '1900-01-01T00:00:00+08:00', 'ProjectId': 10, 'EngineServerId': 1,
                'PresetId': 36, 'QueryLanguageVersionId': 3, 'ScannedLanguageIds': 1073741834,
                'TotalVulnerabilities': 850, 'High': 271, 'Medium': 179, 'Low': 392, 'Info': 8, 'RiskScore': 100,
                'QuantityLevel': 100, 'StatisticsUpdateDate': '2020-11-16T15:05:04.223+08:00', 'StatisticsUpToDate': 1,
                 'IsPublic': True, 'IsLocked': False,
                 'Results': [
                    {'Id': 16, 'ResultId': '1000017-16', 'ScanId': 1000017, 'SimilarityId': 646035161,
                    'RawPriority': None, 'PathId': 16, 'ConfidenceLevel': 0, 'Date': '2020-11-16T15:05:03.273+08:00',
                    'Severity': 'High', 'StateId': 0, 'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None,
                    'QueryId': 589, 'QueryVersionId': 56089346}, {'Id': 17, 'ResultId': '1000017-17', 'ScanId': 1000017,
                     'SimilarityId': -750088295, 'RawPriority': None, 'PathId': 17, 'ConfidenceLevel': 0,
                     'Date': '2020-11-16T15:05:03.277+08:00', 'Severity': 'High', 'StateId': 0,
                     'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None, 'QueryId': 589,
                     'QueryVersionId': 56089346},]
            }]
        """

        relative_url = ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results)&"
                        "$filter=LastScan/Results/"
                        "any(r:%20r/Severity%20eq%20CxDataRepository.Severity%27High%27)")

        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team(
            self, team_id: int, start_date: str, end_date: str
    ) -> List[dict]:
        """
        Requested result:list the number of recurrent/resolved/new issues (vulnerabilities) detected by scans made in
        all projects that were carried out in a team within a predefined time range. The sample query below refers to
        a time range between the 23/07/2015 and 23/08/2015.

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?
        $filter=OwningTeamId%20eq%20%2700000000-1111-1111-b111-989c9070eb11%27&
        $expand=Scans($expand=ResultSummary;$select=Id,ScanRequestedOn,ResultSummary;
        $filter=ScanRequestedOn%20gt%202015-07-23%20and%20ScanRequestedOn%20lt%202015-08-23)

        Returns:
            list of dict

            example:

            [{
            'Id': 10, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
            'CreatedDate': '2020-11-02T04:48:19.783+08:00', 'OwnerId': None, 'OwningTeamId': 1,
            'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
            'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '', 'OriginClientTypeId': 0,
            'PresetId': 36, 'LastScanId': 1000017, 'TotalProjectScanCount': 4, 'SchedulingExpression': None,
            'Scans': [
                {
                'Id': 1000008, 'ScanRequestedOn': '2020-11-02T12:48:19.893+08:00',
                'ResultSummary': {
                                    'ScanId': 1000008,
                                    'PreviousScanId': None,
                                    'New': 908,
                                    'Recurrent': 0,
                                    'Resolved': 0
                                }
                },
                {
                'Id': 1000012, 'ScanRequestedOn': '2020-11-06T16:29:56.147+08:00',
                'ResultSummary': {
                                    'ScanId': 1000012,
                                    'PreviousScanId': 1000008,
                                    'New': 0,
                                    'Recurrent': 908,
                                    'Resolved': 0
                                 }
                },
                ]
            }]
        """

        # OwningTeamId is of type string in 8.9 and previous versions, but from 9.0 the type changed to int
        if get_version_number_as_int() < 900:
            team_id = '%27' + str(team_id) + '%27'

        relative_url = "/Cxwebinterface/odata/v1/Projects?$filter=OwningTeamId%20eq%20{team_id}".format(team_id=team_id)
        relative_url += "&$expand=Scans($expand=ResultSummary;$select=Id,ScanRequestedOn,ResultSummary;"
        relative_url += "$filter=ScanRequestedOn%20gt%20{start_date}%20and".format(start_date=start_date)
        relative_url += "%20ScanRequestedOn%20lt%20{end_date})".format(end_date=end_date)
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_count_of_the_projects_in_the_system(self) -> int:
        """
        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects/$count

        Returns:
            count (int)
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects/$count"

        response = self.api_client.get_request(relative_url=relative_url)
        # value = response.json()
        # return value
        return int(response.content.decode(response.apparent_encoding))

    def get_all_projects_with_a_custom_field_that_has_a_specific_value(
            self, field_name: str, field_value: str
    ) -> List[dict]:
        """
        Requested result: retrieve all projects that contain a custom filed (for example, ProjManager, indicating the
        project manager's name) with a specific value (for example, Joe).

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$filter=CustomFields/any
        (f: f/FieldName eq 'ProjManager' and f/FieldValue eq 'Joe')

        Returns:
            list of dict

            example:
            [
                {
                'Id': 15, 'Name': 'jvl_git', 'IsPublic': True, 'Description': '',
                'CreatedDate': '2020-11-10T02:36:15.42+08:00', 'OwnerId': None, 'OwningTeamId': 1,
                'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
                'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '', 'OriginClientTypeId': 7,
                'PresetId': 36, 'LastScanId': 1000019, 'TotalProjectScanCount': 2, 'SchedulingExpression': None
                }
            ]
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects?$filter=CustomFields/"
        relative_url += "any(f: f/FieldName eq '{field_name}' and f/FieldValue eq '{field_value}')".format(
            field_name=field_name, field_value=field_value
        )
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(
            self, field_name: str
    ) -> List[dict]:
        """
        Requested result: retrieve all projects that contain a custom field (for example, ProjManager, indicating the
        project manager's name), as well as the custom field's information.

        Query used for retrieving the data:
        http://localhost/cxwebinterface/odata/v1/Projects?$expand=CustomFields&$filter=CustomFields/any
        (f: f/FieldName eq 'Field1')

        Returns:
            list of dict

            example:
                [
                    {
                    'Id': 10, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
                    'CreatedDate': '2020-11-02T04:48:19.783+08:00', 'OwnerId': None, 'OwningTeamId': 1,
                    'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
                    'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '',
                    'OriginClientTypeId': 0, 'PresetId': 36, 'LastScanId': 1000017, 'TotalProjectScanCount': 4,
                    'SchedulingExpression': None,
                    'CustomFields': [
                            {'ProjectId': 10, 'FieldName': 'projectManager', 'FieldValue': 'Alex'}
                        ]
                    }
                ]
        """
        relative_url = "/cxwebinterface/odata/v1/Projects?$expand=CustomFields"
        relative_url += "&$filter=CustomFields/any(f: f/FieldName eq '{field_name}')".format(field_name=field_name)

        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_presets_associated_with_each_project(self) -> List[dict]:
        """
        Requested result: retrieves a list of presets associated with each project

        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects?$expand=Preset

        Returns:
            list of dict

            example:
                [
                    {
                    'Id': 10, 'Name': 'jvl_local', 'IsPublic': True, 'Description': '',
                    'CreatedDate': '2020-11-02T04:48:19.783+08:00', 'OwnerId': None, 'OwningTeamId': 1,
                    'EngineConfigurationId': 1, 'IssueTrackingSettings': None, 'SourcePath': '',
                    'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '',
                    'OriginClientTypeId': 0, 'PresetId': 36, 'LastScanId': 1000017, 'TotalProjectScanCount': 4,
                    'SchedulingExpression': None,
                    'Preset': {
                                'Id': 36, 'Name': 'Checkmarx Default', 'IsSystemPreset': True
                            }
                    }
                ]
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects?$expand=Preset"

        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_all_projects_that_are_set_up_with_a_non_standard_configuration(self):
        """
        Requested result: retrieve all projects that are set up with a non-standard configuration,
        such as "Multi-Lanaguage Scan (v8.4.2 and up)".

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId
        or http://localhost/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId%20gt%201

        Returns:
            list of dict

            example:
                [
                    {
                    'Id': 14, 'Name': 'git-ssh', 'IsPublic': True, 'Description': '',
                    'CreatedDate': '2020-11-10T00:47:26.97+08:00', 'OwnerId': None, 'OwningTeamId': 1,
                    'EngineConfigurationId': 5, 'IssueTrackingSettings': None, 'SourcePath': '',
                    'SourceProviderCredentials': '', 'ExcludedFiles': '', 'ExcludedFolders': '',
                    'OriginClientTypeId': 7, 'PresetId': 36, 'LastScanId': None, 'TotalProjectScanCount': 0,
                    'SchedulingExpression': None
                    }
                ]
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId%20gt%201"
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")

    def get_all_projects_id_name(self) -> List[dict]:
        """

        Returns:
            list of dict
            [
                {
                "ProjectId": item.get("Id"),
                "ProjectName": item.get("Name")
                }
            ]
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects?$select=Id,Name"
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json().get("value")
        project_id_name_list = [
            {
                "ProjectId": item.get("Id"),
                "ProjectName": item.get("Name")
            } for item in item_list
        ]

        return project_id_name_list

    def get_all_projects_id_name_and_team_id_name(self) -> List[dict]:
        """

        Returns:

        """
        relative_url = "/Cxwebinterface/odata/v1/Projects?$select=Id,Name,OwningTeamId&$expand=OwningTeam"
        "($select=FullName)"
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json().get("value")
        return [
            {
                "TeamId": item.get('OwningTeamId'),
                "TeamName": item.get('OwningTeam').get('FullName'),
                "ProjectId": item.get("Id"),
                "ProjectName": item.get("Name")
            } for item in item_list
        ]

    def get_all_scan_ids_within_a_predefined_time_range_for_all_projects_in_a_team(
            self, team_id: int, start_date: str, end_date: str
    ) -> List[dict]:
        """
        Requested result:list the number of recurrent/resolved/new issues (vulnerabilities) detected by scans made in
        all projects that were carried out in a team within a predefined time range. The sample query below refers to
        a time range between the 23/07/2015 and 23/08/2015.

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$select=Id,Name&
        $filter=OwningTeamId%20eq%20%2700000000-1111-1111-b111-989c9070eb11%27&
        $expand=Scans($select=Id,ScanRequestedOn;
        $filter=ScanRequestedOn%20gt%202015-07-23%20and%20ScanRequestedOn%20lt%202015-08-23;
        $orderby=Id)

        Returns:
            list of dict
            example:
            [
            {'Id': 5, 'Name': 'jvl_git', 'Scans': [
            {'Id': 1000756}, {'Id': 1000757}, {'Id': 1000762}, {'Id': 1000764}, {'Id': 1000767}, {'Id': 1000773},
            {'Id': 1000775}, {'Id': 1000778}, {'Id': 1000780}, {'Id': 1000781}, {'Id': 1000785}, {'Id': 1000789},
            {'Id': 1000792}, {'Id': 1000795}, {'Id': 1000798}, {'Id': 1000803}, {'Id': 1000810}, {'Id': 1000811},
            {'Id': 1000818}]}
            ]
        """
        # OwningTeamId is of type string in 8.9 and previous versions, but from 9.0 the type changed to int
        if get_version_number_as_int() < 900:
            team_id = '%27' + str(team_id) + '%27'

        relative_url = "/Cxwebinterface/odata/v1/Projects?$select=Id,Name"
        relative_url += "&$filter=OwningTeamId%20eq%20{team_id}".format(team_id=team_id)
        relative_url += "&$expand=Scans($select=Id;"
        relative_url += "$filter=ScanRequestedOn%20gt%20{start_date}%20and".format(start_date=start_date)
        relative_url += "%20ScanRequestedOn%20lt%20{end_date};$orderby=Id)".format(end_date=end_date)
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json()
        return item_list.get("value")


def get_top_n_projects_by_risk_score(number_of_projects: int) -> List[dict]:
    return ProjectsODataAPI().get_top_n_projects_by_risk_score(number_of_projects=number_of_projects)


def get_top_n_projects_by_last_scan_duration(number_of_projects: int) -> List[dict]:
    return ProjectsODataAPI().get_top_n_projects_by_last_scan_duration(number_of_projects=number_of_projects)


def get_all_projects_with_their_last_scan_and_the_high_vulnerabilities():
    return ProjectsODataAPI().get_all_projects_with_their_last_scan_and_the_high_vulnerabilities()


def get_projects_that_have_high_vulnerabilities_in_the_last_scan() -> List[dict]:
    return ProjectsODataAPI().get_projects_that_have_high_vulnerabilities_in_the_last_scan()


def get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id: int, start_date: str, end_date: str
) -> List[dict]:
    return ProjectsODataAPI(
    ).get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id=team_id, start_date=start_date, end_date=end_date
    )


def get_count_of_the_projects_in_the_system() -> int:
    return ProjectsODataAPI().get_count_of_the_projects_in_the_system()


def get_all_projects_with_a_custom_field_that_has_a_specific_value(
        field_name: str, field_value: str
) -> List[dict]:
    return ProjectsODataAPI().get_all_projects_with_a_custom_field_that_has_a_specific_value(
        field_name=field_name, field_value=field_value
    )


def get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(
        field_name: str
) -> List[dict]:
    return ProjectsODataAPI().get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(
        field_name=field_name
    )


def get_presets_associated_with_each_project() -> List[dict]:
    return ProjectsODataAPI().get_presets_associated_with_each_project()


def get_all_projects_that_are_set_up_with_a_non_standard_configuration():
    return ProjectsODataAPI().get_all_projects_that_are_set_up_with_a_non_standard_configuration()


def get_all_projects_id_name() -> List[dict]:
    return ProjectsODataAPI().get_all_projects_id_name()


def get_all_projects_id_name_and_team_id_name() -> List[dict]:
    return ProjectsODataAPI().get_all_projects_id_name_and_team_id_name()


def get_all_scan_ids_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id: int, start_date: str, end_date: str
) -> List[dict]:
    return ProjectsODataAPI().get_all_scan_ids_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id=team_id, start_date=start_date, end_date=end_date
    )
