import json
from .httpRequests import get_request, put_request, post_request, delete_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import PresetPaged, PresetSummary, QueryDetails, Preset
from CheckmarxPythonSDK.utilities.compat import OK

api_url = "/api/presets"


def get_presets(offset=0, limit=10, exact_match=False, include_details=False, name=None):
    """

    Args:
        offset (int):
        limit (int):
        exact_match (bool):
        include_details (bool):
        name (str):

    Returns:

    """
    result = None
    type_check(offset, int)
    type_check(limit, int)
    type_check(exact_match, bool)
    type_check(include_details, bool)
    type_check(name, str)

    relative_url = api_url + (f"/?offset={offset}&limit={limit}&exact_match={exact_match}"
                              f"&include_details={include_details}")
    if name:
        relative_url += f"&name={name}"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = PresetPaged(
            total_count=response.get("totalCount"),
            presets=[
                PresetSummary(
                    preset_id=preset.get("id"),
                    name=preset.get("name"),
                    description=preset.get("description"),
                    associated_projects=preset.get("associatedProjects"),
                    custom=preset.get("custom"),
                    is_tenant_default=preset.get("isTenantDefault"),
                    is_migrated=preset.get("isMigrated"),
                ) for preset in response.get("presets")
            ],
        )
    return result


def create_new_preset(name, description, query_ids):
    """

    Args:
        name (str):
        description (str):
        query_ids (list of str):

    Returns:

    """
    result = None
    type_check(name, str)
    type_check(description, str)
    type_check(query_ids, list)
    list_member_type_check(query_ids, str)

    relative_url = api_url + "/"
    data = json.dumps(
        {
            "name": name,
            "description": description,
            "queryIds": query_ids
        }
    )
    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        response = response.json()
        result = {
            "id": int(response.get("id")),
            "message": response.get("message")
        }
    return result


def get_queries():
    """

    Returns:
        list of QueryDetails
    """
    result = None
    relative_url = api_url + "/queries"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = [
            QueryDetails(
                query_id=query.get("queryID"),
                cwe_id=query.get("cweID"),
                language=query.get("language"),
                group=query.get("group"),
                query_name=query.get("queryName"),
                severity=query.get("severity"),
                query_description_id=query.get("queryDescriptionId"),
                custom=query.get("custom")
            ) for query in response
        ]
    return result


def get_preset_by_id(preset_id):
    """

    Args:
        preset_id (int):

    Returns:

    """
    result = None
    type_check(preset_id, int)
    relative_url = api_url + f"/{preset_id}"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = Preset(
            preset_id=response.get("id"),
            name=response.get("name"),
            description=response.get("description"),
            custom=response.get("custom"),
            query_ids=response.get("queryIds")
        )
    return result


def update_a_preset(preset_id, name, description=None, query_ids=None):
    """

    Args:
        preset_id (int):
        name (str):
        description (str):
        query_ids (list of str):

    Returns:
        dict
        {
          "id": 123456,
          "message": "preset saved"
        }
    """
    result = None
    type_check(preset_id, int)
    type_check(name, str)
    type_check(description, str)
    type_check(query_ids, list)
    list_member_type_check(query_ids, str)

    relative_url = api_url + f"/{preset_id}"

    data = {"name": name,}
    if description:
        data.update({"description": description,})
    if query_ids:
        data.update({"queryIds": query_ids,})

    data = json.dumps(data)

    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        response = response.json()
        result = {
            "id": response.get("id"),
            "message": response.get("message"),
        }
    return result


def delete_a_preset_by_id(preset_id):
    """

        Args:
            preset_id (int):

        Returns:

        """
    is_successful = False
    type_check(preset_id, int)
    relative_url = api_url + f"/{preset_id}"
    response = delete_request(relative_url=relative_url)
    if response.status_code == OK:
        is_successful = True
    return is_successful


def get_preset_summary_by_id(preset_id):
    """

        Args:
            preset_id (int):

        Returns:

        """
    result = None
    type_check(preset_id, int)
    relative_url = api_url + f"/{preset_id}/summary"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = PresetSummary(
            preset_id=response.get("id"),
            name=response.get("name"),
            description=response.get("description"),
            associated_projects=response.get("associatedProjects"),
            custom=response.get("custom"),
            is_tenant_default=response.get("isTenantDefault"),
            is_migrated=response.get("isMigrated"),
        )
    return result


def clone_preset(preset_id, name, description):
    """

        Args:
            preset_id (int):
            name (str):
            description (str):

        Returns:
            dict
        """
    result = None
    type_check(preset_id, int)
    type_check(name, str)
    type_check(description, str)
    relative_url = api_url + f"/{preset_id}/clone"

    data = json.dumps(
        {
            "name": name,
            "description": description,
        }
    )

    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        response = response.json()
        result = {
            "id": response.get("id"),
            "message": response.get("message"),
        }
    return result


def add_query_to_preset(preset_id, query_path):
    """

    Args:
        preset_id (int):
        query_path (str):

    Returns:
        dict
    """
    result = None
    type_check(preset_id, int)
    type_check(query_path, str)

    relative_url = api_url + f"/{preset_id}/add-query"
    data = json.dumps(
        {
            "queryPath": query_path,
        }
    )
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == OK:
        response = response.json()
        result = {
            "id": response.get("id"),
            "message": response.get("message"),
        }
    return result
