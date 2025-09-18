from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import BflTree, construct_sast_result, construct_result_node

api_url = "/api/bfl"


class SastBestFixLocationAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_bfl_graph_by_scan_id(
            self, scan_id: str, query_id: str = None, result_ids: List[str] = None, include_graph: bool = False,
            offset: int = 0, limit: int = 20, apply_predicates: bool = True
    ) -> dict:
        """

       Args:
           scan_id (str): find BFL for scan id
           query_id (str): get BFL from scan id for specific query id
           result_ids (list of str): filter by results id. will include only the selected results ids
                       (OR operator between the items).
           include_graph (bool): If this value is set to true then the trees will contain 2 extra fields -
                       nodes and nodesAdjacencyPairs.
           offset (int): The number of items to skip before starting to collect the result set. Default value : 0
           limit (int): The number of items to return. Default value : 20
           apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw results
                       summary. Default value : true

       Returns:
        dict
       """
        type_check(scan_id, str)
        type_check(query_id, str)
        type_check(result_ids, (list, tuple))
        type_check(include_graph, bool)
        type_check(offset, int)
        type_check(limit, int)
        type_check(apply_predicates, bool)

        list_member_type_check(result_ids, str)

        relative_url = api_url
        params = {"scan-id": scan_id, "query-id": query_id, "result-ids": result_ids, "include-graph": include_graph,
                  "offset": offset, "limit": limit, "apply-predicates": apply_predicates}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return {
            "id": response.get("id"),
            "totalCount": response.get("totalCount"),
            "trees": [
                BflTree(
                    id=tree.get("id"),
                    bfl=construct_result_node(tree.get("bfl")),
                    results=[
                        construct_sast_result(result) for result in tree.get('results') or []
                    ],
                    additional_properties=tree.get("additionalProperties"),
                ) for tree in response.get("trees") or []
            ],
        }


def get_bfl_graph_by_scan_id(
            scan_id: str, query_id: str = None, result_ids: List[str] = None, include_graph: bool = False,
            offset: int = 0, limit: int = 20, apply_predicates: bool = True
) -> dict:
    return SastBestFixLocationAPI().get_bfl_graph_by_scan_id(
        scan_id=scan_id, query_id=query_id, result_ids=result_ids, include_graph=include_graph,
        offset=offset, limit=limit, apply_predicates=apply_predicates
    )
