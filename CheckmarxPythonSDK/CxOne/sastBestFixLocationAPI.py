from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import BflTree, SastResult, construct_result_node

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
                    tree_id=tree.get("id"),
                    bfl=construct_result_node(tree.get("bfl")),
                    results=[
                        SastResult(
                            result_id=result.get('uniqueID'),
                            result_hash=result.get("resultHash"),
                            query_id=result.get("queryID"),
                            query_name=result.get("queryName"),
                            language_name=result.get("languageName"),
                            query_group=result.get("group"),
                            cwe_id=result.get("cweID"),
                            severity=result.get("severity"),
                            similarity_id=result.get("similarityID"),
                            confidence_level=result.get("confidenceLevel"),
                            compliances=result.get("compliances"),
                            first_scan_id=result.get("firstScanID"),
                            first_found_at=result.get("firstFoundAt"),
                            path_system_id_by_simi_and_files_paths=result.get('pathSystemID'),
                            status=result.get("status"),
                            found_at=result.get("foundAt"),
                            nodes=[
                                construct_result_node(node) for node in result.get("nodes") or []
                            ],
                            state=result.get("state"),
                        ) for result in tree.get('results') or []
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
