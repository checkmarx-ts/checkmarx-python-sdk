from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import BflTree


class SastBestFixLocationAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/bfl"
        )

    def get_bfl_graph_by_scan_id(
        self,
        scan_id: str,
        query_id: str = None,
        result_ids: List[str] = None,
        include_graph: bool = False,
        offset: int = 0,
        limit: int = 20,
        apply_predicates: bool = True,
    ) -> dict:
        """
        Args:
            scan_id (str): find BFL for scan id.
            query_id (str): get BFL from scan id for specific query id.
            result_ids (List[str]): filter by results id. OR operator
                between items.
            include_graph (bool): If true, trees will contain extra
                fields - nodes and nodesAdjacencyPairs.
            offset (int): The number of items to skip. Default: 0
            limit (int): The number of items to return. Default: 20
            apply_predicates (bool): If true, apply predicate changes.
                Default: true

        Returns:
            dict
        """
        params = {
            "scan-id": scan_id,
            "query-id": query_id,
            "result-ids": result_ids,
            "include-graph": include_graph,
            "offset": offset,
            "limit": limit,
            "apply-predicates": apply_predicates,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        data = response.json()
        return {
            "id": data.get("id"),
            "totalCount": data.get("totalCount"),
            "trees": [
                BflTree.from_dict(tree)
                for tree in (data.get("trees") or [])
            ],
        }


def get_bfl_graph_by_scan_id(
    scan_id: str,
    query_id: str = None,
    result_ids: List[str] = None,
    include_graph: bool = False,
    offset: int = 0,
    limit: int = 20,
    apply_predicates: bool = True,
) -> dict:
    return SastBestFixLocationAPI().get_bfl_graph_by_scan_id(
        scan_id=scan_id,
        query_id=query_id,
        result_ids=result_ids,
        include_graph=include_graph,
        offset=offset,
        limit=limit,
        apply_predicates=apply_predicates,
    )
