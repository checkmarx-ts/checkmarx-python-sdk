from .HttpRequests import get_request, get_request_with_raw_response
from ..CxPortalSoapApiSDK import get_version_number_as_int


def get_top_n_projects_by_risk_score(number_of_projects):
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

    item_list = get_request(relative_url=relative_url)

    for item in item_list:
        if 'LastScan@odata.context' in item.keys():
            item.pop('LastScan@odata.context')

    return item_list


def get_top_n_projects_by_last_scan_duration(number_of_projects):
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

    item_list = get_request(relative_url=relative_url)

    for item in item_list:
        if 'LastScan@odata.context' in item.keys():
            item.pop('LastScan@odata.context')

    return item_list


def get_all_projects_with_their_last_scan_and_the_high_vulnerabilities():
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
    url = ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results($filter="
           "Severity%20eq%20CxDataRepository.Severity%27High%27))")

    item_list = get_request(relative_url=url)
    for item in item_list:
        if 'LastScan@odata.context' in item.keys():
            item.pop('LastScan@odata.context')
        last_scan = item.get("LastScan")
        if last_scan and 'Results@odata.context' in last_scan.keys():
            last_scan.pop('Results@odata.context')
            
    return item_list


def get_projects_that_have_high_vulnerabilities_in_the_last_scan():
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

    url = ("/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results)&"
           "$filter=LastScan/Results/"
           "any(r:%20r/Severity%20eq%20CxDataRepository.Severity%27High%27)")

    item_list = get_request(relative_url=url)
    for item in item_list:
        if 'LastScan@odata.context' in item.keys():
            item.pop('LastScan@odata.context')
        last_scan = item.get("LastScan")
        if last_scan and 'Results@odata.context' in last_scan.keys():
            last_scan.pop('Results@odata.context')
    
    return item_list


def get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team(
        team_id, start_date, end_date):
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
    item_list = get_request(relative_url=relative_url)

    for item in item_list:
        if 'Scans@odata.context' in item.keys():
            item.pop('Scans@odata.context')
        scans = item.get("Scans")
        for scan in scans:
            if 'ResultSummary@odata.context' in scan.keys():
                scan.pop('ResultSummary@odata.context')

    return item_list


def get_count_of_the_projects_in_the_system():
    """
    Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects/$count

    Returns:
        count (int)
    """
    url = "/Cxwebinterface/odata/v1/Projects/$count"

    r = get_request_with_raw_response(relative_url=url)
    
    return int(r.content.decode(r.apparent_encoding))
    

def get_all_projects_with_a_custom_field_that_has_a_specific_value(field_name, field_value):
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
    return get_request(relative_url=relative_url)


def get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(field_name):
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

    projects = get_request(relative_url=relative_url)
    for project in projects:
        if 'CustomFields@odata.context' in project.keys():
            project.pop('CustomFields@odata.context')

    return projects


def get_presets_associated_with_each_project():
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
    url = "/Cxwebinterface/odata/v1/Projects?$expand=Preset"

    projects = get_request(relative_url=url)
    for project in projects:
        if 'Preset@odata.context' in project.keys():
            project.pop('Preset@odata.context')

    return projects


def get_all_projects_that_are_set_up_with_a_non_standard_configuration():
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
    url = "/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId%20gt%201"

    return get_request(relative_url=url)


def get_all_projects_id_name():
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

    url = "/Cxwebinterface/odata/v1/Projects?$select=Id,Name"

    item_list = get_request(relative_url=url)

    project_id_name_list = [
        {
            "ProjectId": item.get("Id"),
            "ProjectName": item.get("Name")
        } for item in item_list
    ]

    return project_id_name_list


def get_all_projects_id_name_and_team_id_name():
    """

    Returns:

    """
    url = "/Cxwebinterface/odata/v1/Projects?$select=Id,Name,OwningTeamId&$expand=OwningTeam($select=FullName)"

    item_list = get_request(relative_url=url)

    return [
        {
            "TeamId": item.get('OwningTeamId'),
            "TeamName": item.get('OwningTeam').get('FullName'),
            "ProjectId": item.get("Id"),
            "ProjectName": item.get("Name")
        } for item in item_list
    ]
