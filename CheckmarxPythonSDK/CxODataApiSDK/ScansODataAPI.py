from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxODataApiSDK.config import construct_configuration


class ScansODataAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_data_for_a_specific_scan_id(self, scan_id: int) -> dict:
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
        relative_url = "/Cxwebinterface/odata/v1/Scans({id})".format(id=scan_id)
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json().get("value")[0]

    def get_number_of_loc_scanned_for_a_specific_scan(self, scan_id: int) -> int:
        """
        Request result: retrieve LOC scanned value for a specific scan Id
        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Scans(1000005)?$select=LOC

        Args:
            scan_id:

        Returns:
            number_of_loc (int)
        """
        relative_url = "/Cxwebinterface/odata/v1/Scans({id})?$select=LOC".format(id=scan_id)
        response = self.api_client.get_request(relative_url=relative_url)
        loc_list = response.json().get("value")
        return loc_list[0].get('LOC')

    def get_number_of_loc_scanned_for_all_scan(self) -> List[dict]:
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
        relative_url = "/Cxwebinterface/odata/v1/Scans?$select=LOC,Id"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json().get("value")

    def get_last_scan_id_of_a_project(self, project_id: int) -> int:
        """
        http://localhost.checkmarx.net/Cxwebinterface/odata/v1/Projects(4205)/LastScan?$select=Id

        Args:
            project_id (int):

        Returns:
            scan_id (int)
        """
        relative_url = f"/Cxwebinterface/odata/v1/Projects({project_id})//Scans?$orderby=Id%20desc&$top=1&$select=Id"
        response = self.api_client.get_request(relative_url=relative_url)
        ids = response.json().get("value")
        return ids[0].get("Id")

    def get_last_scan_of_a_project(self, project_id: int) -> dict:
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
        relative_url = "/Cxwebinterface/odata/v1/Projects({id})/Scans?$orderby=Id%20desc&$top=1".format(id=project_id)
        response = self.api_client.get_request(relative_url=relative_url)
        scan_data_list = response.json().get("value")
        return scan_data_list[0]

    def get_last_full_scan_id_of_a_project(self, project_id: int) -> int:
        """

        Args:
            project_id (int):

        Returns:
            scan_id (int)
        """
        relative_url = "/Cxwebinterface/odata/v1/Projects({id})/Scans".format(id=project_id)
        relative_url += "?$filter=IsIncremental%20eq%20false&$orderby=Id%20desc&$top=1&select=Id"
        response = self.api_client.get_request(relative_url=relative_url)
        ids = response.json().get("value")
        return ids[0].get("Id")

    def get_last_full_scan_of_a_project(self, project_id: int) -> dict:
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
        response = self.api_client.get_request(relative_url=relative_url)
        scan_data_list = response.json().get("value")
        return scan_data_list[0]

    def get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
            self, project_id: int, start_date: str, end_date: str
    ) -> List[dict]:
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
        return self.api_client.get_request(relative_url=relative_url).json().get("value")

    def get_the_state_of_each_scan_result_since_a_specific_date_for_a_project(
            self, project_id: int, start_date: str
    ) -> List[dict]:
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
        item_list = self.api_client.get_request(relative_url=relative_url).json().get("value")
        return item_list

    def get_all_scan_id_of_a_project(self, project_id: int) -> List[int]:
        """

        Args:
            project_id:

        Returns:
            `list` of int
        """

        url = "/Cxwebinterface/odata/v1/Projects({id})/Scans?$select=Id".format(id=project_id)

        return [item.get('Id') for item in self.api_client.get_request(relative_url=url).json().get("value")]


def get_all_data_for_a_specific_scan_id(scan_id: int) -> dict:
    return ScansODataAPI().get_all_data_for_a_specific_scan_id(scan_id=scan_id)


def get_number_of_loc_scanned_for_a_specific_scan(scan_id: int) -> int:
    return ScansODataAPI().get_number_of_loc_scanned_for_a_specific_scan(scan_id=scan_id)


def get_number_of_loc_scanned_for_all_scan() -> List[dict]:
    return ScansODataAPI().get_number_of_loc_scanned_for_all_scan()


def get_last_scan_id_of_a_project(project_id: int) -> int:
    return ScansODataAPI().get_last_scan_id_of_a_project(project_id=project_id)


def get_last_scan_of_a_project(project_id: int) -> dict:
    return ScansODataAPI().get_last_scan_of_a_project(project_id=project_id)


def get_last_full_scan_id_of_a_project(project_id: int) -> int:
    return ScansODataAPI().get_last_full_scan_id_of_a_project(project_id=project_id)


def get_last_full_scan_of_a_project(project_id: int) -> dict:
    return ScansODataAPI().get_last_full_scan_of_a_project(project_id=project_id)


def get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
        project_id: int, start_date: str, end_date: str
) -> List[dict]:
    return ScansODataAPI().get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
        project_id=project_id, start_date=start_date, end_date=end_date
    )


def get_the_state_of_each_scan_result_since_a_specific_date_for_a_project(
        project_id: int, start_date: str
) -> List[dict]:
    return ScansODataAPI().get_the_state_of_each_scan_result_since_a_specific_date_for_a_project(
        project_id=project_id, start_date=start_date
    )


def get_all_scan_id_of_a_project(project_id: int) -> List[int]:
    return ScansODataAPI().get_all_scan_id_of_a_project(project_id=project_id)
