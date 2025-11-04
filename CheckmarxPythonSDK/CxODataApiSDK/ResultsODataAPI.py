from typing import List, Union
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxODataApiSDK.config import construct_configuration


class ResultsODataAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_results_for_a_specific_scan_id(self, scan_id: int) -> List[dict]:
        """
        http://localhost/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=0
        http://localhost/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=10

        Args:
            scan_id (int):

        Returns:
            `list` of `dict`

            example:
            [
            {
            'Id': 4, 'ResultId': '1000012-4', 'ScanId': 1000012, 'SimilarityId': 1937265109, 'RawPriority': None,
            'PathId': 4, 'ConfidenceLevel': 95, 'Date': '2020-11-06T16:32:07.603+08:00', 'Severity': 'High',
            'StateId': 0,
            'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None, 'QueryId': 589, 'QueryVersionId': 56089346
            }
            ]
        """

        url = "/Cxwebinterface/odata/v1/Scans({ScanId})/Results".format(
            ScanId=scan_id
        )

        response = self.api_client.get_request(relative_url=url)
        return response.json().get("value")

    def get_the_query_that_was_run_for_a_particular_unique_scan_result(
            self, result_id: int, scan_id: int
    ) -> Union[str, None]:
        """
        Requested result: selects a particular unique scan result and lists the query (SQL Injection, etc.) that was run

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Results(Id=18,ScanId=1000001)?$expand=Query($select=Name)

         Args:
            result_id (int):
            scan_id (int):

        Returns:
            str
        """
        relative_url = "/Cxwebinterface/odata/v1/Results(Id={id},ScanId={ScanId})".format(id=result_id, ScanId=scan_id)
        relative_url += "?$expand=Query($select=Name)"
        response = self.api_client.get_request(relative_url=relative_url)
        query_list = response.json().get("value")

        if not query_list:
            return None

        return query_list[0].get("Query").get("Name")

    def get_results_for_a_specific_scan_id_with_query_language_state(
            self, scan_id: int, filter_false_positive: bool = False
    ) -> List[dict]:
        """

        might need to read in page mode

        Args:
            scan_id (int):
            filter_false_positive (bool): filter False positive (eg. only choose [Propose] Not Exploitable)

        Returns:
            list of dict

            example:
            [
            {
            'ResultId': 2, 'QueryId': 589, 'QueryName': 'Connection_String_Injection',
            'QueryGroupName': 'Java_High_Risk', 'LanguageName': 'Java', 'StateName': 'Not Exploitable'
            },
            {
            'ResultId': 73, 'QueryId': 591, 'QueryName': 'Reflected_XSS_All_Clients',
            'QueryGroupName': 'Java_High_Risk', 'LanguageName': 'Java', 'StateName': 'To Verify'
            }
            ]
        """
        # have to put ScanId in url, otherwise would have deserialization error
        relative_url = "/Cxwebinterface/odata/v1/Scans({id})/Results".format(id=scan_id)
        relative_url += "?$select=Id,ScanId,QueryId,SimilarityId,PathId&$expand=Query($select=Name;"
        relative_url += "$expand=QueryGroup($select=Name,LanguageName)),State($select=Name),Scan($select=Origin,LOC)"

        if filter_false_positive:
            relative_url += "&$filter=State/Id eq 1 or State/Id eq 4"

        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json().get("value")

        results = [
            {
                "SimilarityId": item.get("SimilarityId"),
                "Language": item.get("Query").get("QueryGroup").get("LanguageName"),
                "QueryGroup": item.get("Query").get("QueryGroup").get("Name"),
                "Query": item.get("Query").get("Name"),
                "QueryId": item.get("QueryId"),
                "ResultId": item.get("Id"),
                "ResultState": item.get("State").get("Name"),
                "Origin": item.get("Scan").get("Origin"),
                "LOC": item.get("Scan").get("LOC"),
                "PathId": item.get("PathId"),
            } for item in item_list
        ]

        results = sorted(results, key=lambda re: (re.get("Language"), re.get("QueryGroup"),
                                                  re.get("QueryId"), re.get("ResultId"),))
        return results

    def get_results_group_by_query_id_and_add_count_json_format(
            self, scan_id: int, filter_false_positive: bool = False, threshold: int = 0
    ) -> List[dict]:
        """

        Args:
            scan_id (int):
            filter_false_positive (bool):
            threshold (int): minimum value of Count

        Returns:

        """
        re = self.get_results_for_a_specific_scan_id_with_query_language_state(
            scan_id=scan_id, filter_false_positive=filter_false_positive
        )

        results = []

        from itertools import groupby
        # first group by LanguageName
        re = sorted(re, key=lambda result: result.get("Language"))
        for _, language_group in groupby(re, lambda result: result.get("Language")):
            l_list = list(language_group)
            language_name = l_list[0].get("Language")
            query_group_list = []
            results.append(
                {
                    "Language": language_name,
                    "QueryGroupList": query_group_list
                }
            )

            # second group by QueryGroupName
            l_list = sorted(l_list, key=lambda result: result.get("QueryGroup"))
            for _, query_group_group in groupby(l_list, lambda result: result.get("QueryGroup")):
                l_query_group = list(query_group_group)
                query_group_name = l_query_group[0].get("QueryGroup")
                query_list = []
                query_group_list.append(
                    {
                        "QueryGroup": query_group_name,
                        "QueryList": query_list
                    }
                )

                # third group by QueryName/QueryId
                l_query_group = sorted(l_query_group, key=lambda r: r.get("QueryId"))
                for _, query_group in groupby(l_query_group, lambda r: r.get("QueryId")):
                    l_query_name = list(query_group)
                    query_name = l_query_name[0].get("Query")

                    count = len(l_query_name)
                    # ignore those queries that count smaller than threshold
                    if count < threshold:
                        continue

                    query_list.append(
                        {
                            "Query": query_name,
                            "Count": count
                        }
                    )

        return results

    def get_results_for_a_specific_scan_id_with_similarity_ids(
            self, scan_id: int, similarity_ids: List[int]
    ) -> List[dict]:
        """

        might need to read in page mode

        Args:
            scan_id (int):
            similarity_ids (`list` of int)


        Returns:
            list of dict

            example:
            [
            {
            'ResultId': 66, 'ScanId': 1000008, 'SimilarityId': -1403228976, 'RawPriority': None, 'PathId': 66,
            'ConfidenceLevel': 96, 'Date': '2022-02-09T10:56:38.433+08:00', 'Severity': 'High', 'StateId': 0,
            'AssignedToUserId': None, 'AssignedTo': None, 'Comment': None, 'QueryId': 595, 'QueryVersionId': 56163505,
            'Language': 'Java', 'QueryGroup': 'Java_High_Risk', 'Query': 'Stored_XSS', 'ResultState': 'To Verify',
             'Origin': 'Checkmarx Python SDK 0.4.2', 'LOC': 6912
             }
            ]
        $select=Id,ScanId,QueryId,SimilarityId,PathId
        """

        # have to put ScanId in url, otherwise would have deserialization error
        url = "/Cxwebinterface/odata/v1/Scans({id})/Results?".format(
            id=scan_id
        )

        url += "&$expand=Query($select=Name;$expand=QueryGroup($select=Name," \
               " LanguageName)),State($select=Name),Scan($select=Origin,LOC)"

        url += "&$filter=SimilarityId in ({similarity_id_list})".format(
            similarity_id_list=",".join([str(item) for item in similarity_ids])
        )

        response = self.api_client.get_request(relative_url=url)
        item_list = response.json().get("value")

        results = [
            {
                "ResultId": item.get("Id"),
                'ScanId': item.get("ScanId"),
                "SimilarityId": item.get("SimilarityId"),
                'RawPriority': item.get("RawPriority"),
                "PathId": item.get("PathId"),
                'ConfidenceLevel': item.get("ConfidenceLevel"),
                'Date': item.get("Date"),
                'Severity': item.get("Severity"),
                'StateId': item.get("StateId"),
                'AssignedToUserId': item.get("AssignedToUserId"),
                'AssignedTo': item.get("AssignedTo"),
                'Comment': item.get("Comment"),
                "QueryId": item.get("QueryId"),
                'QueryVersionId': item.get("QueryVersionId"),
                "Language": item.get("Query").get("QueryGroup").get("LanguageName"),
                "QueryGroup": item.get("Query").get("QueryGroup").get("Name"),
                "Query": item.get("Query").get("Name"),
                "ResultState": item.get("State").get("Name"),
                "Origin": item.get("Scan").get("Origin"),
                "LOC": item.get("Scan").get("LOC"),
            } for item in item_list
        ]
        return results

    def get_number_of_results_for_a_specific_scan_id_with_result_state(
            self, scan_id: int, result_states: List[str]
    ) -> int:
        """

        Args:
            scan_id (int):
            result_states (list of str): Available values,
                TO_VERIFY, NOT_EXPLOITABLE, CONFIRMED, URGENT, PROPOSED_NOT_EXPLOITABLE

        Returns:
            int

        """
        for state in result_states:
            if state not in ["TO_VERIFY", "NOT_EXPLOITABLE", "CONFIRMED", "URGENT", "PROPOSED_NOT_EXPLOITABLE"]:
                raise ValueError("result state should be in the list: TO_VERIFY, NOT_EXPLOITABLE, CONFIRMED, URGENT, "
                                 "PROPOSED_NOT_EXPLOITABLE")
        state_index_map = {
            "TO_VERIFY": 0,
            "NOT_EXPLOITABLE": 1,
            "CONFIRMED": 2,
            "URGENT": 3,
            "PROPOSED_NOT_EXPLOITABLE": 4
        }
        state_id_list = [state_index_map.get(item) for item in result_states]

        relative_url = "/Cxwebinterface/odata/v1/Scans({id})/Results".format(id=scan_id)
        relative_url += "?$select=Id&$filter=State/Id in ({state_id_list})".format(
            state_id_list=",".join([str(item) for item in state_id_list])
        )
        response = self.api_client.get_request(relative_url=relative_url)
        item_list = response.json().get("value")
        return len(item_list)

    def get_similarity_ids_of_a_scan(self, scan_id: int) -> List[dict]:
        relative_url = f"/Cxwebinterface/odata/v1/Scans({scan_id})/Results?$select=SimilarityId,PathId"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json().get("value")


def get_results_for_a_specific_scan_id(scan_id: int) -> List[dict]:
    return ResultsODataAPI().get_results_for_a_specific_scan_id(scan_id=scan_id)


def get_the_query_that_was_run_for_a_particular_unique_scan_result(
        result_id: int, scan_id: int
) -> Union[str, None]:
    return ResultsODataAPI().get_the_query_that_was_run_for_a_particular_unique_scan_result(
        result_id=result_id, scan_id=scan_id
    )


def get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id: int, filter_false_positive: bool = False
) -> List[dict]:
    return ResultsODataAPI().get_results_for_a_specific_scan_id_with_query_language_state(
        scan_id=scan_id, filter_false_positive=filter_false_positive
    )


def get_results_group_by_query_id_and_add_count_json_format(
        scan_id: int, filter_false_positive: bool = False, threshold: int = 0
) -> List[dict]:
    return ResultsODataAPI().get_results_group_by_query_id_and_add_count_json_format(
        scan_id=scan_id, filter_false_positive=filter_false_positive, threshold=threshold
    )


def get_results_for_a_specific_scan_id_with_similarity_ids(
        scan_id: int, similarity_ids: List[int]
) -> List[dict]:
    return ResultsODataAPI().get_results_for_a_specific_scan_id_with_similarity_ids(
        scan_id=scan_id, similarity_ids=similarity_ids
    )


def get_number_of_results_for_a_specific_scan_id_with_result_state(
        scan_id: int, result_states: List[str]
) -> int:
    return ResultsODataAPI().get_number_of_results_for_a_specific_scan_id_with_result_state(
        scan_id=scan_id, result_states=result_states
    )


def get_similarity_ids_of_a_scan(scan_id: int) -> List[dict]:
    return ResultsODataAPI().get_similarity_ids_of_a_scan(scan_id=scan_id)
