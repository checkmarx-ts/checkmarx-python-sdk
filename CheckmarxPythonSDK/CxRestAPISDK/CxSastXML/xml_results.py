from os.path import exists
from xml.etree.ElementTree import Element
from .dto import (
    CxXMLResults,
    construct_cx_xml_results,
    Line,
    construct_line,
    Path,
    construct_path,
    PathNode,
    construct_path_node,
    Query,
    construct_query,
    Result,
    construct_result,
    Snippet,
    construct_snippet,
)


def construct_object_element_tree(root) -> CxXMLResults:
    """

    Args:
        root (Element):

    Returns:

    """
    queries = []
    query_tags = list(root)
    for query_tag in query_tags:
        results = []
        result_tags = list(query_tag)
        for result_tag in result_tags:
            path_tags = list(result_tag)
            path_tag = path_tags[0]
            path_nodes = []
            path_node_tags = list(path_tag)
            for path_node_tag in path_node_tags:
                file_name = path_node_tag[0].text
                line_number = path_node_tag[1].text
                column_number = path_node_tag[2].text
                node_id = path_node_tag[3].text
                node_name = path_node_tag[4].text
                node_type = path_node_tag[5].text
                node_name_length = path_node_tag[6].text
                if len(path_node_tag) >= 8:
                    snippet_tag = path_node_tag[7]
                    line_tags = list(snippet_tag)
                    line_tag = line_tags[0]
                    inner_line_number = line_tag[0].text
                    code = line_tag[1].text
                    line = construct_line(number=inner_line_number, code=code)
                    snippet = construct_snippet(line)
                else:
                    snippet = None
                path_node = construct_path_node(
                    file_name=file_name,
                    line_number=line_number,
                    column_number=column_number,
                    node_id=node_id,
                    node_name=node_name,
                    node_type=node_type,
                    node_name_length=node_name_length,
                    snippet=snippet
                )
                path_nodes.append(path_node)
            path = construct_path(item=path_tag.attrib, path_nodes=path_nodes)
            result = construct_result(item=result_tag.attrib, path=path)
            results.append(result)
        query = construct_query(item=query_tag.attrib, results=results)
        queries.append(query)
    return construct_cx_xml_results(root.attrib, queries=queries)


def get_xml_results(xml_file_path=None, xml_content_as_string=None) -> CxXMLResults:
    """

    Args:
        xml_file_path (str):
        xml_content_as_string (str):

    Returns:
        CxXMLResults
    """
    if not xml_file_path and not xml_content_as_string:
        return None

    import xml.etree.ElementTree as ET
    root = None
    if xml_file_path and exists(xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    if xml_content_as_string:
        root = ET.fromstring(xml_content_as_string)
    return construct_object_element_tree(root)


def obj_to_dict(obj) -> dict:
    result = {}
    if isinstance(obj, (int, str, bool, dict)):
        return obj
    obj_dict = obj.__dict__
    for key, value in obj_dict.items():
        if value is None or isinstance(value, (int, str)):
            if key == 'schema':
                key = '$schema'
            result[key] = value
        elif isinstance(value, list):
            result[key] = []
            for item in value:
                result[key].append(obj_to_dict(item))
        else:
            result[key] = obj_to_dict(value)

    return result


def get_xml_results_as_dict(xml_file_path=None, xml_content_as_string=None) -> dict:
    result = get_xml_results(
        xml_file_path=xml_file_path, xml_content_as_string=xml_content_as_string
    )
    return obj_to_dict(result)

