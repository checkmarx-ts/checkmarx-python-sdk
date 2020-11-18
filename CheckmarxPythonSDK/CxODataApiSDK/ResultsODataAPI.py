import requests

from ..config import config
from . import authHeaders
from ..compat import (OK, UNAUTHORIZED)
from .dto import construct_result_data


class ResultsODataAPI(object):

    def __init__(self):
        self.retry = 0

    def get_results_for_a_specific_scan_id(self, scan_id):
        """
        http://localhost/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=0
        http://localhost/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=10

        Args:
            scan_id (int):

        Returns:
            `list` of `dict`
        """
        results = None
        url = config.get("base_url") + "/Cxwebinterface/odata/v1/Scans({ScanId})/Results".format(
            ScanId=scan_id
        )

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            results = [construct_result_data(item) for item in item_list]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_results_for_a_specific_scan_id(scan_id)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return results

    def get_the_query_that_was_run_for_a_particular_unique_scan_result(self, result_id, scan_id):
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
        query_name = None

        url = config.get("base_url") + ("/Cxwebinterface/odata/v1/Results(Id={id},ScanId={ScanId})"
                                        "?$expand=Query($select=Name)").format(
            id=result_id,
            ScanId=scan_id
        )

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            query_name = r.json().get('value')[0].get("Query").get("Name")
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_the_query_that_was_run_for_a_particular_unique_scan_result(result_id, scan_id)
        else:
            raise ValueError(r.text)

        self.retry = 0

        return query_name

    def get_results_for_a_specific_scan_id_with_query_language_state(self, scan_id, filter_false_positive=False):
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
        results = []
        # have to put ScanId in url, otherwise would have deserialization error
        url = config.get("base_url") + ("/Cxwebinterface/odata/v1/Scans({id})/Results?$select=Id,ScanId,QueryId"
                                        "&$expand=Query($select=Name;$expand=QueryGroup($select=Name,"
                                        "LanguageName)),State($select=Name)").format(
            id=scan_id
        )

        if filter_false_positive:
            url += "&$filter=State/Id eq 1 or State/Id eq 4"

        r = requests.get(
            url=url,
            headers=authHeaders.auth_headers,
            auth=authHeaders.basic_auth,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            item_list = r.json().get('value')
            results = [
                {
                    "Language": item.get("Query").get("QueryGroup").get("LanguageName"),
                    "QueryGroup": item.get("Query").get("QueryGroup").get("Name"),
                    "Query": item.get("Query").get("Name"),
                    "QueryId": item.get("QueryId"),
                    "ResultId": item.get("Id"),
                    "ResultState": item.get("State").get("Name")
                } for item in item_list
            ]
        elif r.status_code == UNAUTHORIZED and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_results_for_a_specific_scan_id_with_query_language_state(scan_id, filter_false_positive)
        else:
            raise ValueError(r.text)

        self.retry = 0

        results = sorted(results, key=lambda re: (re.get("ResultId"), re.get("Language"), re.get("QueryGroup"),
                                                  re.get("QueryId")))
        return results

    def get_results_group_by_query_id_and_add_count_json_format(self, scan_id, filter_false_positive=False,
                                                                threshold=0):
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
