import requests

from ..config import config
from . import authHeaders
from ..compat import (OK, UNAUTHORIZED)


class ScansODataAPI(object):

    def __init__(self):
        self.retry = 0

    def retrieve_all_data_for_a_specific_scan_id(self, scan_id):
        """
        Request result: retrieve all data for a specific scan Id:
        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Scans(1000005)

        Args:
            scan_id (int):

        Returns:
            dict or None
        """
        scan_data = None

        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Scans({id})".format(id=scan_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json().get('value')[0]
            scan_data = {
                "Id": item.get("Id"),
                "SourceId": item.get("SourceId"),
                "Comment": item.get("Comment"),
                "IsIncremental": item.get("IsIncremental"),
                "ScanType": item.get("ScanType"),
                "Origin": item.get("Origin"),
                "OwnerId": item.get("OwnerId"),
                "OwningTeamId": item.get("OwningTeamId"),
                "InitiatorName": item.get("InitiatorName"),
                "ProjectName": item.get("ProjectName"),
                "PresetName": item.get("PresetName"),
                "TeamName": item.get("TeamName"),
                "Path": item.get("Path"),
                "FileCount": item.get("FileCount"),
                "LOC": item.get("LOC"),
                "FailedLOC": item.get("FailedLOC"),
                "ProductVersion": item.get("ProductVersion"),
                "IsForcedScan": item.get("IsForcedScan"),
                "ScanRequestedOn": item.get("ScanRequestedOn"),
                "QueuedOn": item.get("QueuedOn"),
                "EngineStartedOn": item.get("EngineStartedOn"),
                "EngineFinishedOn": item.get("EngineFinishedOn"),
                "ScanCompletedOn": item.get("ScanCompletedOn"),
                "ScanDuration": item.get("ScanDuration"),
                "ProjectId": item.get("ProjectId"),
                "EngineServerId": item.get("EngineServerId"),
                "PresetId": item.get("PresetId"),
                "QueryLanguageVersionId": item.get("QueryLanguageVersionId"),
                "ScannedLanguageIds": item.get("ScannedLanguageIds"),
                "TotalVulnerabilities": item.get("TotalVulnerabilities"),
                "High": item.get("High"),
                "Medium": item.get("Medium"),
                "Low": item.get("Low"),
                "Info": item.get("Info"),
                "RiskScore": item.get("RiskScore"),
                "QuantityLevel": item.get("QuantityLevel"),
                "StatisticsUpdateDate": item.get("StatisticsUpdateDate"),
                "StatisticsUpToDate": item.get("StatisticsUpToDate"),
                "IsPublic": item.get("IsPublic"),
                "IsLocked": item.get("IsLocked"),
            }
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.retrieve_all_data_for_a_specific_scan_id(scan_id)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return scan_data

    def retrieve_number_of_loc_scanned_for_a_specific_scan(self, scan_id):
        """
        Request result: retrieve LOC scanned value for a specific scan Id
        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Scans(1000005)?$select=LOC

        Args:
            scan_id:

        Returns:
            int or None
        """
        number_of_loc = None

        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Scans({id})?$select=LOC".format(id=scan_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json().get('value')[0]
            number_of_loc = item.get('LOC')
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.retrieve_number_of_loc_scanned_for_a_specific_scan(scan_id)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return number_of_loc

    def retrieve_number_of_loc_scanned_for_all_scan(self):
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
        loc_id_pair_list = []

        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Scans?$select=LOC,Id"
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            loc_id_pair_list = item_list
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.retrieve_number_of_loc_scanned_for_all_scan()
        else:
            raise ValueError(r.text)

        self.retry = 0

        return loc_id_pair_list

    def get_the_scan_id_of_last_scan(self, project_id):
        """
        http://localhost.checkmarx.net/Cxwebinterface/odata/v1/Projects(4205)/LastScan?$select=Id

        Args:
            project_id (int):

        Returns:
            int
        """
        scan_id = None

        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Projects({id})/LastScan?$select=Id".format(
            id=project_id
        )

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item = r.json().get('value')[0]
            scan_id = item.get("Id")
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_the_scan_id_of_last_scan(project_id)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return scan_id

    def get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
            self, project_id, start_date, end_date
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
                [
                {
                    'Id': 1000014,
                    'ScanRequestedOn': '2020-11-10T10:36:17.34+08:00',
                    'High': 278,
                    'Medium': 193,
                    'Low': 422
                 }
                ]
        """
        scan_list = []

        url = config.get("base_url") + ("/Cxwebinterface/odata/v1/Projects({id})/Scans?"
                                        "$filter=ScanRequestedOn%20gt%20{start_date}%20and"
                                        "%20ScanRequestedOn%20lt%20{end_date}"
                                        "&$select=Id,ScanRequestedOn,High,Medium,Low"
                                        "&$orderby=ScanRequestedOn%20desc").format(
            id=project_id, start_date=start_date, end_date=end_date
        )

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            scan_list = r.json().get('value')
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project(
                project_id, start_date, end_date)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return scan_list

    def get_the_state_of_each_scan_result_since_a_specific_date_for_a_project(self, project_id):
        """
        Requested result: for a specific project, list all the scans starting from a specific date, and for each scan
        retrieve three parameters (Id, ScanId, and StateId) as well as the state of each of the scan's vulnerabilities
        that was found in scans since the specified date.

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Scans?
        $filter=ProjectId%20eq%2011%20and%20ScanRequestedOn%20gt%202014-12-31&
        $expand=Results($expand=State;$select=Id,ScanId,StateId)

        Returns:

        """

    def get_all_scan_id_of_a_project(self, project_id):
        """

        Args:
            project_id:

        Returns:
            `list` of int
        """
        scan_id_list = []

        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Projects({id})/Scans?$select=Id".format(id=project_id)
        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            scan_id_list = [item.get('Id') for item in item_list]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_scan_id_of_a_project(project_id)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return scan_id_list
