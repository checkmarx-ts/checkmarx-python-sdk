# encoding: utf-8
"""
    Portal SOAP API
    Only support 9.x version.
    Start from 9.0, Portal SOAP API needs Bear Token for authentication
"""

from . import zeepClient
from ..config import config
from . import authHeaders


def retry_when_unauthorized(func):
    """

    Args:
        func (function)

    Returns:
        function
    """
    def retry(*args, **kwargs):
        max_try = config.get('max_try')

        response = func(*args, **kwargs)

        while max_try > 0:
            if response.IsSuccesfull:
                break

            # message id "12563" means invalid token
            if not response.IsSuccesfull and '12563' in response.ErrorMessage:
                authHeaders.update_auth_headers()
                zeepClient.client, zeepClient.factory = zeepClient.get_client_and_factory()
                response = func(*args, **kwargs)
            max_try -= 1

        return response
    return retry


def add_license_expiration_notification():
    """

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.AddLicenseExpirationNotification(sessionID="0")

    r = execute()

    return {
        "IsSuccesfull": r["IsSuccesfull"],
        "ErrorMessage": r["ErrorMessage"]
    }


def create_new_preset(query_ids, name):
    """

    Args:
        query_ids (`list` of int):
        name (str):

    Returns:
        dict

        sample return:
        {
            'queryIds':  [
                    343
            ],
            'id': 110003,
            'name': 'ddd',
            'owningteam': 1,
            'isPublic': True,
            'owner': None,
            'isUserAllowToUpdate': True,
            'isUserAllowToDelete': True,
            'IsDuplicate': False
        }
    """
    @retry_when_unauthorized
    def execute():

        query_id_list = zeepClient.factory.ArrayOfLong(query_ids)

        cx_preset_detail = zeepClient.factory.CxPresetDetails(
            queryIds=query_id_list, id=0, name=name, owningteam=1, isPublic=True,
            isUserAllowToUpdate=True, isUserAllowToDelete=True, IsDuplicate=False
        )

        return zeepClient.client.service.CreateNewPreset(sessionId="0", presrt=cx_preset_detail)

    r = execute()
    preset = r.preset
    return {
        "IsSuccesfull": r["IsSuccesfull"],
        "ErrorMessage": r["ErrorMessage"],
        "preset": {
            'queryIds':  preset["queryIds"]["long"],
            'id': preset["id"],
            'name': preset["name"],
            'owningteam': preset["owningteam"],
            'isPublic': preset["isPublic"],
            'owner': preset["owner"],
            'isUserAllowToUpdate': preset["isUserAllowToUpdate"],
            'isUserAllowToDelete': preset["isUserAllowToDelete"],
            'IsDuplicate': preset["IsDuplicate"]
        } if preset else None
    }


def delete_preset(preset_id):
    """

    Args:
        preset_id (int):

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.DeletePreset(sessionId="0", id=preset_id)

    p = execute()
    return {
        "IsSuccesfull": p["IsSuccesfull"],
        "ErrorMessage": p["ErrorMessage"]
    }


def delete_project(project_id):
    """

    Args:
        project_id (int):

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.DeleteProject(sessionID="0", projectID=project_id)

    p = execute()
    return {
        "IsSuccesfull": p["IsSuccesfull"],
        "ErrorMessage": p["ErrorMessage"]
    }


def delete_projects(project_ids, flag="None"):
    """

    Args:
        project_ids (list of int):
        flag (str): "None", "RunningScans", "OnlyAllowedProjects"

    Returns:
        bool
    """

    @retry_when_unauthorized
    def execute():
        cx_ws_request_delete_projects = zeepClient.factory.CxWSRequestDeleteProjects(
            SessionID="0",
            ProjectIDs=zeepClient.factory.ArrayOfLong(project_ids),
            Flags=zeepClient.factory.DeleteFlags([flag])
        )
        return zeepClient.client.service.DeleteProjects(request=cx_ws_request_delete_projects)

    p = execute()
    return {
        "IsSuccesfull": p["IsSuccesfull"],
        "ErrorMessage": p["ErrorMessage"],
        "Flags": p["Flags"],
        "IsConfirmation": p["IsConfirmation"],
        "NumOfDeletedProjects": p["NumOfDeletedProjects"],
        "UndeletedProjects": p["UndeletedProjects"]
    }


def get_path_comments_history(scan_id, path_id, label_type):
    """

    Args:
        scan_id (int):
        path_id (int):
        label_type (str):

    Returns:
        dict

        example:
        {
            'IsSuccesfull': True,
            'ErrorMessage': None,
            'Path': {
                'SimilarityId': 0,
                'PathId': 0,
                'Comment': 'happy yang jvl_local, [2020年11月12日 16:57]: Changed status to Not Exploitable
                            happy yang jvl_local, [2020年11月12日 16:57]: Changed status to Proposed Not Exploitable ÿ',
                'State': 0,
                'Severity': 0,
                'AssignedUser': None,
                'Nodes': None
            }
        }
    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.GetPathCommentsHistory(sessionId="0", scanId=scan_id, pathId=path_id,
                                                                labelType=label_type)

    r = execute()
    path = r.Path
    return {
        "IsSuccesfull": r["IsSuccesfull"],
        "ErrorMessage": r["ErrorMessage"],
        "Path": {
            "AssignedUser": path["AssignedUser"],
            "Comment": path["Comment"],
            "Nodes": path["Nodes"],
            "PathId": path["PathId"],
            "Severity": path["Severity"],
            "SimilarityId": path["SimilarityId"],
            "State": path["State"]
        } if path else None
    }


def get_name_of_user_who_marked_false_positive_from_comments_history(scan_id, path_id):
    """

    Args:
        scan_id (int):
        path_id (int):

    Returns:
        first_and_last_name (str)
        example:
         "happy yang"
    """
    comments_history = get_path_comments_history(scan_id, path_id, label_type="Remark").get("Path").get("Comment")

    if "ÿ" not in comments_history:
        return None

    a_list = comments_history.split('ÿ')[0:-1]
    second_list = [item.split(',')[0] for item in a_list if 'Not Exploitable' in item]
    name_and_project = second_list[0]
    d_list = name_and_project.split(" ")
    e_list = d_list[0:2]
    return " ".join(e_list)


def get_preset_list():
    """

    Returns:
        list of dict
    """

    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.GetPresetList(SessionID="0")

    r = execute()
    preset_list = r.PresetList
    return {
        "IsSuccesfull": r["IsSuccesfull"],
        "ErrorMessage": r["ErrorMessage"],
        "PresetList": [
            {
                "PresetName": item["PresetName"],
                "ID": item["ID"],
                "owningUser": item["owningUser"],
                "isUserAllowToUpdate": item["isUserAllowToUpdate"],
                "isUserAllowToDelete": item["isUserAllowToDelete"]
            } for item in preset_list["Preset"]
        ] if preset_list else None
    }


def get_server_license_data():
    """

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.GetServerLicenseData(sessionID="0")

    p = execute()
    supported_languages = p.SupportedLanguages
    return {
        "ExpirationDate": p["ExpirationDate"],
        "MaxConcurrentScans": p["MaxConcurrentScans"],
        "MaxLOC": p["MaxLOC"],
        "HID": p["HID"],
        "SupportedLanguages": [{
            "isSupported": item["isSupported"],
            "language": item["language"]
            } for item in supported_languages["SupportedLanguage"]
        ] if supported_languages else None,
        "MaxUsers": p["MaxUsers"],
        "CurrentUsers": p["CurrentUsers"],
        "MaxAuditUsers": p["MaxAuditUsers"],
        "CurrentAuditUsers": p["CurrentAuditUsers"],
        "IsOsaEnabled": p["IsOsaEnabled"],
        "OsaExpirationDate": p["OsaExpirationDate"],
        "Edition": p["Edition"],
        "ProjectsAllowed": p["ProjectsAllowed"],
        "CurrentProjectsCount": p["CurrentProjectsCount"]
    }


def get_server_license_summary():
    """

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.GetServerLicenseSummary(sessionID="0")

    p = execute()
    supported_languages = p.SupportedLanguages
    return {
        "ExpirationDate": p["ExpirationDate"],
        "MaxConcurrentScans": p["MaxConcurrentScans"],
        "MaxLOC": p["MaxLOC"],
        "HID": p["HID"],
        "SupportedLanguages": [{
            "isSupported": item["isSupported"],
            "language": item["language"]
            } for item in supported_languages["SupportedLanguage"]
        ] if supported_languages else None,
        "MaxUsers": p["MaxUsers"],
        "CurrentUsers": p["CurrentUsers"],
        "MaxAuditUsers": p["MaxAuditUsers"],
        "CurrentAuditUsers": p["CurrentAuditUsers"],
        "IsOsaEnabled": p["IsOsaEnabled"],
        "OsaExpirationDate": p["OsaExpirationDate"],
        "Edition": p["Edition"],
        "ProjectsAllowed": p["ProjectsAllowed"],
        "CurrentProjectsCount": p["CurrentProjectsCount"]
    }


def get_version_number():
    """

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        return zeepClient.client.service.GetVersionNumber()

    p = execute()
    return {
        "IsSuccesfull": p["IsSuccesfull"],
        "ErrorMessage": p["ErrorMessage"],
        "Version": p["Version"]
    }
