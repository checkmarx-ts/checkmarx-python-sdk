import json
from .httpRequests import get_request, patch_request, post_request, put_request, delete_request
from .utilities import type_check, list_member_type_check
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .dto import (
    DefaultConfig,
    DefaultConfigOut,
    ScanParameter,
)

api_url = "/api/configuration"


def get_the_list_of_all_the_parameters_defined_for_the_current_tenant():
    relative_url = api_url + "/tenant"
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        ScanParameter(
            key=item.get("key"),
            name=item.get("name"),
            category=item.get("category"),
            origin_level=item.get("originLevel"),
            value=item.get("value"),
            value_type=item.get("valueType"),
            value_type_params=item.get("valueTypeParams"),
            allow_override=item.get("allowOverride")
        ) for item in response
    ]


def define_parameters_in_the_input_list_for_the_current_tenant(scan_parameters):
    """

    Args:
        scan_parameters (list of ScanParameter):

    Returns:

    """
    type_check(scan_parameters, (list, tuple))
    list_member_type_check(scan_parameters, ScanParameter)

    result = False
    relative_url = api_url + "/tenant"
    data = json.dumps([scan_parameter.to_dict() for scan_parameter in scan_parameters])
    response = patch_request(relative_url=relative_url, data=data)
    if response.status == NO_CONTENT:
        result = True
    return result


def delete_parameters_for_a_tenant(config_keys):
    """

    Args:
        config_keys (str):

    Returns:

    """
    result = False
    relative_url = api_url + "/tenant?config-keys={}".format(config_keys)
    response = delete_request(relative_url=relative_url)
    if response.status == NO_CONTENT:
        result = True
    return result


def get_the_list_of_all_the_parameters_for_a_project(project_id):
    """

    Args:
        project_id (str):

    Returns:

    """
    type_check(project_id, str)
    relative_url = api_url + "/project?project-id=" + project_id
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        ScanParameter(
            key=item.get("key"),
            name=item.get("name"),
            category=item.get("category"),
            origin_level=item.get("originLevel"),
            value=item.get("value"),
            value_type=item.get("valueType"),
            value_type_params=item.get("valueTypeParams"),
            allow_override=item.get("allowOverride")
        ) for item in response
    ]


def define_parameters_in_the_input_list_for_a_specific_project(project_id, scan_parameters):
    """

        Args:
            project_id (str):
            scan_parameters (list of ScanParameter):

        Returns:

        """
    result = False
    type_check(project_id, str)
    relative_url = api_url + "/project?project-id=" + project_id
    data = json.dumps([scan_parameter.to_dict() for scan_parameter in scan_parameters])
    response = patch_request(relative_url=relative_url, data=data)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def delete_parameters_for_a_specific_project(project_id, config_keys):
    """

    Args:
        project_id (str):
        config_keys (str):

    Returns:

    """
    result = False
    type_check(project_id, str)
    type_check(config_keys, str)
    relative_url = api_url + "/project?project-id={}&config-keys={}".format(project_id, config_keys)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run(project_id, scan_id):
    """

    Args:
        project_id (str):
        scan_id (str):

    Returns:

    """
    type_check(project_id, str)
    type_check(scan_id, str)
    relative_url = api_url + "/scan?project-id={}&scan-id={}".format(project_id, scan_id)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        ScanParameter(
            key=item.get("key"),
            name=item.get("name"),
            category=item.get("category"),
            origin_level=item.get("originLevel"),
            value=item.get("value"),
            value_type=item.get("valueType"),
            value_type_params=item.get("valueTypeParams"),
            allow_override=item.get("allowOverride")
        ) for item in response
    ]


def get_all_default_configs_for_the_tenant(name=None, exact_match=None, limit=100, offset=0):
    """

    Args:
        name (str, optional): Filter by default config name
        exact_match (bool, optional): Forces the filter query to be an exact match instead
        limit (int): Limits the number of returned results. Default value : 100
        offset (int): Offset from which start returned results. Default value : 0

    Returns:

    """
    type_check(name, str)
    type_check(exact_match, bool)
    type_check(limit, int)
    type_check(offset, int)
    relative_url = api_url + "/sast/default-config"
    response = get_request(relative_url=relative_url)
    response = response.json()
    return [
        DefaultConfigOut(
            default_config_out_id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            url=item.get("url"),
            is_tenant_default=item.get("isTenantDefault"),
            associated_projects=item.get("associatedProjects")
        ) for item in response
    ]


def create_a_default_config_for_the_sast_engine(default_config):
    """

    Args:
        default_config (DefaultConfig):

    Returns:

    """
    result = False
    type_check(default_config, DefaultConfig)
    relative_url = api_url + "/sast/default-config"
    data = json.dumps(default_config.to_dict())
    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def get_sast_default_config_by_id(config_id):
    """

    Args:
        config_id (str):

    Returns:

    """
    type_check(config_id, str)
    relative_url = api_url + "/sast/default-config/{id}".format(id=config_id)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return DefaultConfigOut(
        default_config_out_id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        url=item.get("url"),
        is_tenant_default=item.get("isTenantDefault"),
        associated_projects=item.get("associatedProjects")
    )


def update_default_config_for_the_sast_engine(config_id, default_config):
    """

    Args:
        config_id (str):
        default_config (DefaultConfig):

    Returns:

    """
    result = False
    type_check(config_id, str)
    type_check(default_config, DefaultConfig)
    relative_url = api_url + "/sast/default-config/{id}".format(id=config_id)
    data = json.dumps(default_config.to_dict())
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def delete_a_sast_default_config(config_id):
    """

        Args:
            config_id (str):

        Returns:

        """
    result = False
    type_check(config_id, str)
    relative_url = api_url + "/sast/default-config/{id}".format(id=config_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def update_project_repo_url(project_id, repo_url):
    """

    Args:
        project_id (str):
        repo_url (str):

    Returns:

    """
    result = False
    type_check(project_id, str)
    type_check(repo_url, str)
    relative_url = api_url + "/project?project-id=" + project_id
    data = [{
        "key": "scan.handler.git.repository",
        "name": "repository",
        "category": "git",
        "originLevel": "Project",
        "value": repo_url,
        "valuetype": "String",
        "allowOverride": True
    }]

    data_json = json.dumps(data)
    response = patch_request(relative_url=relative_url, data=data_json)

    if response.status_code == NO_CONTENT:
        result = True
    return result


def update_project_token(project_id, token):
    """

    Args:
        project_id (str):
        token (str):

    Returns:

    """
    result = False
    type_check(project_id, str)
    type_check(token, str)
    relative_url = api_url + "/project?project-id=" + project_id
    data = [{
        "key": "scan.handler.git.token",
        "name": "token",
        "category": "git",
        "originLevel": "Project",
        "value": token,
        "valuetype": "Secret",
        "allowOverride": True
    }, ]

    data_json = json.dumps(data)
    response = patch_request(relative_url=relative_url, data=data_json)

    if response.status_code == NO_CONTENT:
        result = True
    return result
