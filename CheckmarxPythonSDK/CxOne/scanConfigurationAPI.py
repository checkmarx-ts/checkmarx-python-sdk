import json
from .httpRequests import get_request, patch_request
from .utilities import get_url_param, type_check, list_member_type_check
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .dto import (
    DefaultConfig,
    DefaultConfigOut,
    Error,
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
    data = json.dumps([scan_parameter.get_post_data(return_raw_dict=True) for scan_parameter in scan_parameters])
    response = patch_request(relative_url=relative_url, data=data)
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
    data = json.dumps([scan_parameter.get_post_data(return_raw_dict=True) for scan_parameter in scan_parameters])
    response = patch_request(relative_url=relative_url, data=data)
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
