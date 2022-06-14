from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import BflTree, SastResult, ResultNode

api_url = "/api/bfl"


def get_bfl_graph_by_scan_id(scan_id, query_id=None, result_ids=None, include_graph=False, offset=0, limit=20,
                             apply_predicates=True):
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

    """
    type_check(scan_id, str)
    type_check(query_id, str)
    type_check(result_ids, (list, tuple))
    type_check(include_graph, bool)
    type_check(offset, int)
    type_check(limit, int)
    type_check(apply_predicates, bool)

    list_member_type_check(result_ids, str)

    relative_url = api_url + "?scan-id={scan_id}".format(scan_id=scan_id)
    relative_url += get_url_param("query-id", query_id)
    relative_url += get_url_param("result-ids", result_ids)
    relative_url += get_url_param("include-graph", include_graph)
    relative_url += get_url_param("offset", offset)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("apply-predicates", apply_predicates)

    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "id": response.get("id"),
        "totalCount": response.get("totalCount"),
        "trees": [
            BflTree(
                tree_id=tree.get("id"),
                bfl=ResultNode(
                    column=tree.get("bfl").get('column'),
                    file_name=tree.get("bfl").get('fileName'),
                    full_name=tree.get("bfl").get('fullName'),
                    length=tree.get("bfl").get('length'),
                    line=tree.get("bfl").get('line'),
                    method_line=tree.get("bfl").get('methodLine'),
                    method=tree.get("bfl").get('method'),
                    name=tree.get("bfl").get('name'),
                    dom_type=tree.get("bfl").get('domType')
                ),
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
                            ResultNode(
                                column=node.get("column"),
                                file_name=node.get('fileName'),
                                full_name=node.get('fullName'),
                                length=node.get('length'),
                                line=node.get('line'),
                                method_line=node.get('methodLine'),
                                method=node.get("method"),
                                name=node.get('name'),
                                dom_type=node.get('domType'),
                            ) for node in result.get("nodes") or []
                        ],
                        state=result.get("state"),
                    ) for result in tree.get('results') or []
                ],
                additional_properties=tree.get("additionalProperties"),
            ) for tree in response.get("trees") or []
        ],
    }
