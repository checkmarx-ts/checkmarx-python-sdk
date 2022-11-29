from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import SastResult, ResultNode

api_url = "/api/sast-results"


def get_sast_results_by_scan_id(scan_id, severity=None, status=None, query_group=None, compliance=None, query=None,
                                language=None, query_ids=None, node_ids=None, source_file=None,
                                source_file_operation=None, source_node=None, source_node_operation=None,
                                sink_node=None, sink_node_operation=None, sink_file=None, sink_file_operation=None,
                                include_nodes=True, apply_predicates=True, offset=0, limit=20, sort=None):
    """

    Args:
        scan_id (str): filter by scan id
        severity (list of str): filter by severity. OR operator between the items.
                        Available values : HIGH, MEDIUM, LOW, INFO
        status (list of str): filter by status. OR operator between the items.
                        Available values : NEW, RECURRENT, FIXED
        query_group (str): filter by group. matching groups that CONTAINES the input.
        compliance (str): filter by compliance. matching groups that EQUALS the input with case insensitive.
        query (str): filter by query. matching queries that EQUALS the input.
        language (list of str): filter by language name. matching languages that EQUALS the input with case insensitive.
        query_ids (list of str): filter by queries ids. matching queries that EQUALS to the inputs.
        node_ids (list of str): Node IDs to find. OR operator between the items.
        source_file (str): filter by source file name.
        source_file_operation (str): filter operation for source file.
                        Available values : CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL
        source_node (str): filter by source node
        source_node_operation (str): filter operation for source node
                        Available values : CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL
        sink_node (str): filter by sink node
        sink_node_operation (str): filter operation for sink node
                        Available values : CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL
        sink_file (str): filter by sink file name
        sink_file_operation (str): filter operation for sink file
                        Available values : CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL
        include_nodes (bool): if true returns ResultNode objects, otherwise will omit the Nodes field.
                        Default value : true
        apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw result.
                        Default value : true
        offset (int): The number of items to skip before starting to collect the result set.
                        Default value : 0
        limit (int): The number of items to return.
                        Default value : 20
        sort (list of str): sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                        Available values : -severity, +severity, -status, +status, -firstfoundat, +firstfoundat,
                        -foundat, +foundat, -queryname, +queryname, -firstscanid, +firstscanid
                        Default value : List [ "+status", "+severity", "-queryname" ]

    Returns:
        dict
    """

    type_check(scan_id, str)
    type_check(severity, (list, tuple))
    type_check(status, (list, tuple))
    type_check(query_group, str)
    type_check(compliance, str)
    type_check(query, str)
    type_check(language, (list, tuple))
    type_check(query_ids, (list, tuple))
    type_check(node_ids, (list, tuple))
    type_check(source_file, str)
    type_check(source_file_operation, str)
    type_check(source_node, str)
    type_check(source_node_operation, str)
    type_check(sink_node, str)
    type_check(sink_node_operation, str)
    type_check(sink_file, str)
    type_check(sink_file_operation, str)
    type_check(include_nodes, bool)
    type_check(apply_predicates, bool)
    type_check(offset, int)
    type_check(limit, int)
    type_check(sort, (list, tuple))

    list_member_type_check(severity, str)
    list_member_type_check(status, str)
    list_member_type_check(language, str)
    list_member_type_check(query_ids, str)
    list_member_type_check(node_ids, str)
    list_member_type_check(sort, str)

    relative_url = api_url + "?scan-id={scan_id}".format(scan_id=scan_id)
    relative_url += get_url_param("severity", severity)
    relative_url += get_url_param("status", status)

    relative_url += get_url_param("status", status)
    relative_url += get_url_param("status", status)
    relative_url += get_url_param("group", query_group)
    relative_url += get_url_param("compliance", compliance)
    relative_url += get_url_param("query", query)
    relative_url += get_url_param("language", language)
    relative_url += get_url_param("query-ids", query_ids)
    relative_url += get_url_param("node-ids", node_ids)
    relative_url += get_url_param("source-file", source_file)
    relative_url += get_url_param("source-file-operation", source_file_operation)
    relative_url += get_url_param("source-node", source_node)
    relative_url += get_url_param("source-node-operation", source_node_operation)
    relative_url += get_url_param("sink-node", sink_node)
    relative_url += get_url_param("sink-node-operation", sink_node_operation)
    relative_url += get_url_param("sink-file", sink_file)
    relative_url += get_url_param("sink-file-operation", sink_file_operation)
    relative_url += get_url_param("include-nodes", include_nodes)
    relative_url += get_url_param("apply-predicates", apply_predicates)
    relative_url += get_url_param("offset", offset)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("sort", sort)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "results": [
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
            ) for result in response.get("results") or []
        ],
        "totalCount": response.get("totalCount")
    }
