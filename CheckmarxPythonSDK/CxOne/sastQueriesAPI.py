from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import QueriesResponse, Preset, QueryDescription, QueryDescriptionSampleCode, Category, CategoryType
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED

query_url = "/api/queries"


def get_list_of_the_existing_query_repos():
    """

    Returns:
        list of QueriesResponse
    """
    relative_url = query_url
    response = get_request(relative_url=relative_url)
    queries = response.json()
    return [
        QueriesResponse(
            name=item.get("name"),
            is_active=item.get("isActive"),
            last_modified=item.get("lastModified"),
        ) for item in queries
    ]


def get_sast_queries_presets(project_id=None):
    """

    Args:
        project_id (str):

    Returns:
        list of Preset
    """
    relative_url = query_url + "/presets"
    relative_url += get_url_param("project-id", project_id)
    response = get_request(relative_url=relative_url)
    presets = response.json()
    return [
        Preset(
            preset_id=item.get("id"),
            name=item.get("name"),
        ) for item in presets
    ]


def get_sast_query_description(ids):
    """

    Args:
        ids (list of str): list of query ids

    Returns:
        list of QueryDescription
         associated to each of the given query ids
    """
    type_check(ids, list)
    list_member_type_check(ids, str)

    relative_url = query_url + "/descriptions?"
    relative_url += get_url_param("ids", ids)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        QueryDescription(
            query_description_id=item.get("queryDescriptionId"),
            result_description=item.get("resultDescription"),
            risk=item.get("risk"),
            cause=item.get("cause"),
            general_recommendations=item.get("generalRecommendations"),
            samples=[
                QueryDescriptionSampleCode(
                    programming_language=sample.get("progLanguage"),
                    code=sample.get("code"),
                    title=sample.get("title"),
                ) for sample in item.get("samples") or []
            ],
        ) for item in response or []
    ]


def get_mapping_between_ast_and_sast_query_ids():
    """

    Returns:
        list of dict
        [
        {
          "astId": "string",
          "sastId": "string"
        }
      ]
    """
    result = None
    relative_url = query_url + "/mappings"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response.json().get("mappings")
    return result


def get_sast_queries_preset_for_a_specific_scan(scan_id):
    """

    Args:
        scan_id (str):

    Returns:
        prest_id (int)
    """
    result = None
    relative_url = query_url + f"/preset/{scan_id}"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response.json().get("id")
    return result


def get_sast_queries_categories():
    """

    Returns:
        list of CategoryType
    """
    result = None
    relative_url = query_url + "/categories-types"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = [
            CategoryType(
                category_type_id=item.get("id"),
                name=item.get("name"),
                sast_id=item.get("sastId"),
                order=item.get("order"),
                categories=[
                    Category(
                        category_id=category.get("id"),
                        name=category.get("name"),
                        sast_id=category.get("sastId"),
                    ) for category in item.get("categories", []) or []
                ]
            ) for item in response
        ]
    return result
