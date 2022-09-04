from .HttpRequests import get_request


def get_all_data_for_a_specific_scan_id(scan_id):
    """
    Request result: retrieve all data for a specific scan Id:
    Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Scans(1000005)

    Args:
        scan_id (int):

    Returns:
        dict or None

        example:
        {
        'Id': 1000019, 'SourceId': '0000000069_001929049475_0-1940062284', 'Comment': '', 'IsIncremental': False,
        'ScanType': 1, 'Origin': 'Web Portal', 'OwnerId': None, 'OwningTeamId': 1, 'InitiatorName': 'happy yang',
        'ProjectName': 'jvl_git', 'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer',
        'Path': 'https://github.com/CSPF-Founder/JavaVulnerableLab.git', 'FileCount': 69, 'LOC': 6912,
        'FailedLOC': 0, 'ProductVersion': '9.2.0.41015 HF6', 'IsForcedScan': False,
        'ScanRequestedOn': '2020-11-17T14:10:48.877+08:00', 'QueuedOn': '2020-11-17T14:11:07.187+08:00',
        'EngineStartedOn': '2020-11-17T14:11:23.837+08:00', 'EngineFinishedOn': '2020-11-17T14:12:38.007+08:00',
        'ScanCompletedOn': '2020-11-17T14:12:38.06+08:00', 'ScanDuration': '1900-01-01T00:01:14.223+08:00',
        'ProjectId': 15, 'EngineServerId': 1, 'PresetId': 36, 'QueryLanguageVersionId': 3,
        'ScannedLanguageIds': 1073741834, 'TotalVulnerabilities': 901, 'High': 278, 'Medium': 193, 'Low': 422,
        'Info': 8, 'RiskScore': 100, 'QuantityLevel': 100, 'StatisticsUpdateDate': '2020-11-17T14:12:38.153+08:00',
        'StatisticsUpToDate': 1, 'IsPublic': True, 'IsLocked': False
        }
    """

    url = "/Cxwebinterface/odata/v1/Scans({id})".format(id=scan_id)

    scan_data_list = get_request(relative_url=url)

    if not scan_data_list:
        return None

    return scan_data_list[0]


def get_number_of_loc_scanned_for_a_specific_scan(scan_id):
    """
    Request result: retrieve LOC scanned value for a specific scan Id
    Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Scans(1000005)?$select=LOC

    Args:
        scan_id:

    Returns:
        number_of_loc (int)
    """

    url = "/Cxwebinterface/odata/v1/Scans({id})?$select=LOC".format(id=scan_id)

    loc_list = get_request(relative_url=url)

    if not loc_list:
        return None

    return loc_list[0].get('LOC')


def get_number_of_loc_scanned_for_all_scan():
    """
    Request result: retrieve LOC scanned value for all scans
    Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Scans?$select=LOC,Id

    Returns:
        list of dict

        example:
        [
         {'LOC': 6907, 'Id': 1000008}, {'LOC': 6912, 'Id': 1000012}, {'LOC': 6907, 'Id': 1000016},
         {'LOC': 6907, 'Id': 1000017}, {'LOC': 6912, 'Id': 1000014}, {'LOC': 2161, 'Id': 1000015},
         {'LOC': 6907, 'Id': 1000018}
        ]
    """

    url = "/Cxwebinterface/odata/v1/Scans?$select=LOC,Id"

    return get_request(relative_url=url)


def get_last_scan_id_of_a_project(project_id):
    """
    http://localhost.checkmarx.net/Cxwebinterface/odata/v1/Projects(4205)/LastScan?$select=Id

    Args:
        project_id (int):

    Returns:
        scan_id (int)
    """

    url = "/Cxwebinterface/odata/v1/Projects({id})//Scans?$orderby=Id%20desc&$top=1&$select=Id".format(id=project_id)

    ids = get_request(relative_url=url)

    if not ids:
        return None

    return ids[0].get("Id")


def get_last_scan_of_a_project(project_id):
    """
    http://localhost.checkmarx.net/Cxwebinterface/odata/v1/Projects(4205)/LastScan

    Args:
        project_id (int):

    Returns:
        dict

        example:
        {
        'Id': 1000019, 'SourceId': '0000000069_001929049475_0-1940062284', 'Comment': '', 'IsIncremental': False,
        'ScanType': 1, 'Origin': 'Web Portal', 'OwnerId': None, 'OwningTeamId': 1, 'InitiatorName': 'happy yang',
        'ProjectName': 'jvl_git', 'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer',
        'Path': 'https://github.com/CSPF-Founder/JavaVulnerableLab.git', 'FileCount': 69, 'LOC': 6912,
        'FailedLOC': 0, 'ProductVersion': '9.2.0.41015 HF6', 'IsForcedScan': False,
        'ScanRequestedOn': '2020-11-17T14:10:48.877+08:00', 'QueuedOn': '2020-11-17T14:11:07.187+08:00',
        'EngineStartedOn': '2020-11-17T14:11:23.837+08:00', 'EngineFinishedOn': '2020-11-17T14:12:38.007+08:00',
        'ScanCompletedOn': '2020-11-17T14:12:38.06+08:00', 'ScanDuration': '1900-01-01T00:01:14.223+08:00',
        'ProjectId': 15, 'EngineServerId': 1, 'PresetId': 36, 'QueryLanguageVersionId': 3,
        'ScannedLanguageIds': 1073741834, 'TotalVulnerabilities': 901, 'High': 278, 'Medium': 193, 'Low': 422,
        'Info': 8, 'RiskScore': 100, 'QuantityLevel': 100, 'StatisticsUpdateDate': '2020-11-17T14:12:38.153+08:00',
        'StatisticsUpToDate': 1, 'IsPublic': True, 'IsLocked': False
        }

    """
    url = "/Cxwebinterface/odata/v1/Projects({id})/Scans?$orderby=Id%20desc&$top=1".format(id=project_id)

    scan_data_list = get_request(relative_url=url)

    if not scan_data_list:
        return None

    return scan_data_list[0]


def get_last_full_scan_id_of_a_project(project_id):
    """

    Args:
        project_id (int):

    Returns:
        scan_id (int)
    """
    relative_url = "/Cxwebinterface/odata/v1/Projects({id})/Scans".format(id=project_id)
    relative_url += "?$filter=IsIncremental%20eq%20false&$orderby=Id%20desc&$top=1&select=Id"

    ids = get_request(relative_url=relative_url)

    if not ids:
        return None

    return ids[0].get("Id")


def get_last_full_scan_of_a_project(project_id):
    """

    Args:
        project_id (int):

    Returns:
        dict

        example:
        {
        'Id': 1000019, 'SourceId': '0000000069_001929049475_0-1940062284', 'Comment': '', 'IsIncremental': False,
        'ScanType': 1, 'Origin': 'Web Portal', 'OwnerId': None, 'OwningTeamId': 1, 'InitiatorName': 'happy yang',
        'ProjectName': 'jvl_git', 'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer',
        'Path': 'https://github.com/CSPF-Founder/JavaVulnerableLab.git', 'FileCount': 69, 'LOC': 6912,
        'FailedLOC': 0, 'ProductVersion': '9.2.0.41015 HF6', 'IsForcedScan': False,
        'ScanRequestedOn': '2020-11-17T14:10:48.877+08:00', 'QueuedOn': '2020-11-17T14:11:07.187+08:00',
        'EngineStartedOn': '2020-11-17T14:11:23.837+08:00', 'EngineFinishedOn': '2020-11-17T14:12:38.007+08:00',
        'ScanCompletedOn': '2020-11-17T14:12:38.06+08:00', 'ScanDuration': '1900-01-01T00:01:14.223+08:00',
        'ProjectId': 15, 'EngineServerId': 1, 'PresetId': 36, 'QueryLanguageVersionId': 3,
        'ScannedLanguageIds': 1073741834, 'TotalVulnerabilities': 901, 'High': 278, 'Medium': 193, 'Low': 422,
        'Info': 8, 'RiskScore': 100, 'QuantityLevel': 100, 'StatisticsUpdateDate': '2020-11-17T14:12:38.153+08:00',
        'StatisticsUpToDate': 1, 'IsPublic': True, 'IsLocked': False
        }
    """
    relative_url = "/Cxwebinterface/odata/v1/Projects({id})/Scans".format(id=project_id)
    relative_url += "?$filter=IsIncremental%20eq%20false&$orderby=Id%20desc&$top=1"
    
    scan_data_list = get_request(relative_url=relative_url)

    if not scan_data_list:
        return None

    return scan_data_list[0]


def get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
    project_id, start_date, end_date
):
    """
    Requested result:list all scans carried out in a specific project within a predefined time range,
    as well as their H/M/L (High/Medium/Low) values. The sample query below refers to a time range
    between the 23/07/2015 and 23/08/2015.

    Query used for retrieving the data:
    http://localhost/Cxwebinterface/odata/v1/Projects(11)/Scans?
    $filter=ScanRequestedOn%20gt%202015-07-23%20and%20ScanRequestedOn%20lt%202015-08-23&
    $select=Id,ScanRequestedOn,High,Medium,Low&$orderby=ScanRequestedOn%20desc

    Args:
        project_id (int):
        start_date (str): example: '2015-07-23'
        end_date (str): example: '2015-08-23'

    Returns:
        list of dict

        Example:
            [{
                'Id': 1000014,
                'ScanRequestedOn': '2020-11-10T10:36:17.34+08:00',
                'High': 278,
                'Medium': 193,
                'Low': 422
             }]
    """

    relative_url = "/Cxwebinterface/odata/v1/Projects({id})/Scans?".format(id=project_id)
    relative_url += "$filter=ScanRequestedOn%20gt%20{start_date}%20and".format(start_date=start_date)
    relative_url += "%20ScanRequestedOn%20lt%20{end_date}".format(end_date=end_date)
    relative_url += "&$select=Id,ScanRequestedOn,High,Medium,Low&$orderby=ScanRequestedOn%20desc"
    return get_request(relative_url=relative_url)


def get_the_state_of_each_scan_result_since_a_specific_date_for_a_project(project_id, start_date):
    """
    Requested result: for a specific project, list all the scans starting from a specific date, and for each scan
    retrieve three parameters (Id, ScanId, and StateId) as well as the state of each of the scan's vulnerabilities
    that was found in scans since the specified date.

    Query used for retrieving the data:
    http://localhost/Cxwebinterface/odata/v1/Scans?
    $filter=ProjectId%20eq%2011%20and%20ScanRequestedOn%20gt%202014-12-31&
    $expand=Results($expand=State;$select=Id,ScanId,StateId)
    Args:
        project_id (int):
        start_date (str): example: '2015-07-23'

    Returns:
        list of dict

        example:
        [{
        'Id': 1000019, 'SourceId': '0000000069_001929049475_0-1940062284',
        'Comment': '', 'IsIncremental': False, 'ScanType': 1, 'Origin': 'Web Portal', 'OwnerId': None,
        'OwningTeamId': 1, 'InitiatorName': 'happy yang', 'ProjectName': 'jvl_git',
        'PresetName': 'Checkmarx Default', 'TeamName': 'CxServer',
        'Path': 'https://github.com/CSPF-Founder/JavaVulnerableLab.git',
        'FileCount': 69, 'LOC': 6912, 'FailedLOC': 0, 'ProductVersion': '9.2.0.41015 HF6',
        'IsForcedScan': False, 'ScanRequestedOn': '2020-11-17T14:10:48.877+08:00',
        'QueuedOn': '2020-11-17T14:11:07.187+08:00', 'EngineStartedOn': '2020-11-17T14:11:23.837+08:00',
        'EngineFinishedOn': '2020-11-17T14:12:38.007+08:00', 'ScanCompletedOn': '2020-11-17T14:12:38.06+08:00',
        'ScanDuration': '1900-01-01T00:01:14.223+08:00', 'ProjectId': 15, 'EngineServerId': 1, 'PresetId': 36,
        'QueryLanguageVersionId': 3, 'ScannedLanguageIds': 1073741834, 'TotalVulnerabilities': 901,
        'High': 278, 'Medium': 193, 'Low': 422, 'Info': 8, 'RiskScore': 100, 'QuantityLevel': 100,
        'StatisticsUpdateDate': '2020-11-17T14:12:38.153+08:00', 'StatisticsUpToDate': 1, 'IsPublic': True,
        'IsLocked': False,
        'Results': [{'Id': 86, 'State': 'To Verify'}, {'Id': 826, 'State': 'To Verify'}]
        }]
    """

    relative_url = "/Cxwebinterface/odata/v1/Scans?"
    relative_url += "$filter=ProjectId%20eq%20{id}%20and".format(id=project_id)
    relative_url += "%20ScanRequestedOn%20gt%20{start_date}".format(start_date=start_date)
    relative_url += "&$expand=Results($expand=State;$select=Id,ScanId,StateId)"
    item_list = get_request(relative_url=relative_url)

    for item in item_list:
        if 'Results@odata.context' in item.keys():
            item.pop('Results@odata.context')
        results = item.get('Results')
        for result in results:
            if 'State@odata.context' in result.keys():
                result.pop('State@odata.context')

    return item_list


def get_all_scan_id_of_a_project(project_id):
    """

    Args:
        project_id:

    Returns:
        `list` of int
    """

    url = "/Cxwebinterface/odata/v1/Projects({id})/Scans?$select=Id".format(id=project_id)

    return [item.get('Id') for item in get_request(relative_url=url)]
