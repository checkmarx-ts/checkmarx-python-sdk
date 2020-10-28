# encoding: utf-8
"""
    Portal SOAP API
"""

from . import zeepClient
from ..config import config


def retry_if_token_is_invalid(response, execute_func, retry_times):
    """

    Args:
        response ():
        execute_func (func):
        retry_times (list of int):

    Returns:

    """
    # message id "12563" means invalid token
    if not response.IsSuccesfull and '12563' in response.ErrorMessage and retry_times[0] < config.get("max_try"):
        retry_times[0] += 1
        # get new token and create new client and factory
        zeepClient.client, zeepClient.factory = zeepClient.get_client_and_factory()
        execute_func()


def activate_saas_user(user_token):
    """
    This action is no longer supported in CxSAST 9.2.
    Args:
        user_token (str):

    Returns:

    """
    retry_times = [0]

    def execute():
        response = zeepClient.client.service.ActivateSaasUser(userToken=user_token)
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

    r = execute()

    return {
        "IsSuccesfull": r["IsSuccesfull"],
        "ErrorMessage": r["ErrorMessage"],
        "IsAllowedToUseSourceControl": r["IsAllowedToUseSourceControl"],
        "isAllowedToCreatePDF": r["isAllowedToCreatePDF"],
        "IsAllowedToUseOnlineViewer": r["IsAllowedToUseOnlineViewer"],
        "IsAllowedToUsePlugins": r["IsAllowedToUsePlugins"],
        "IsAllowedToViewResultState": r["IsAllowedToViewResultState"],
        "IsAllowedToEditResultState": r["IsAllowedToEditResultState"],
        "IsAllowedToViewResultSeverity": r["IsAllowedToViewResultSeverity"],
        "IsAllowedToEditResultSeverity": r["IsAllowedToEditResultSeverity"],
        "IsAllowedToViewAssignTo": r["IsAllowedToViewAssignTo"],
        "IsAllowedToEditAssignTo": r["IsAllowedToEditAssignTo"],
        "IsAllowedToViewComments": r["IsAllowedToViewComments"],
        "IsAllowedToEditComments": r["IsAllowedToEditComments"]
    }


def add_license_expiration_notification():
    """

    Returns:

    """
    retry_times = [0]

    def execute():
        response = zeepClient.client.service.AddLicenseExpirationNotification(sessionID="0")
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

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
    retry_times = [0]

    def execute():

        query_id_list = zeepClient.factory.ArrayOfLong(query_ids)
        cx_preset_detail = zeepClient.factory.CxPresetDetails(
            queryIds=query_id_list, id=0, name=name, owningteam=1, isPublic=True,
            isUserAllowToUpdate=True, isUserAllowToDelete=True, IsDuplicate=False
        )

        response = zeepClient.client.service.CreateNewPreset(sessionId="0", presrt=cx_preset_detail)
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

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
    retry_times = [0]

    def execute():

        response = zeepClient.client.service.DeletePreset(sessionId="0", id=preset_id)
        retry_if_token_is_invalid(response, execute, retry_times)
        return response
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
    retry_times = [0]

    def execute():
        response = zeepClient.client.service.DeleteProject(sessionID="0", projectID=project_id)
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

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
    retry_times = [0]

    def execute():

        cx_ws_request_delete_projects = zeepClient.factory.CxWSRequestDeleteProjects(
            SessionID="0",
            ProjectIDs=zeepClient.factory.ArrayOfLong(project_ids),
            Flags=zeepClient.factory.DeleteFlags([flag])
        )
        response = zeepClient.client.service.DeleteProjects(request=cx_ws_request_delete_projects)
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

    p = execute()
    return {
        "IsSuccesfull": p["IsSuccesfull"],
        "ErrorMessage": p["ErrorMessage"],
        "Flags": p["Flags"],
        "IsConfirmation": p["IsConfirmation"],
        "NumOfDeletedProjects": p["NumOfDeletedProjects"],
        "UndeletedProjects": p["UndeletedProjects"]
    }


def get_preset_list():
    """

    Returns:
        list of dict
    """
    retry_times = [0]

    def execute():

        response = zeepClient.client.service.GetPresetList(SessionID="0")
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

    r = execute()
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
            } for item in r["PresetList"]["Preset"]
        ] if r["PresetList"] else None
    }


def get_server_license_data():
    """

    Returns:

    """
    retry_times = [0]

    def execute():
        response = zeepClient.client.service.GetServerLicenseData(sessionID="0")
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

    p = execute()
    return {
        "ExpirationDate": p["ExpirationDate"],
        "MaxConcurrentScans": p["MaxConcurrentScans"],
        "MaxLOC": p["MaxLOC"],
        "HID": p["HID"],
        "SupportedLanguages": [{
            "isSupported": item["isSupported"],
            "language": item["language"]
        }
            for item in p["SupportedLanguages"]["SupportedLanguage"]
        ],
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
    retry_times = [0]

    def execute():
        response = zeepClient.client.service.GetServerLicenseSummary(sessionID="0")
        retry_if_token_is_invalid(response, execute, retry_times)
        return response

    p = execute()
    return {
        "ExpirationDate": p["ExpirationDate"],
        "MaxConcurrentScans": p["MaxConcurrentScans"],
        "MaxLOC": p["MaxLOC"],
        "HID": p["HID"],
        "SupportedLanguages": [{
            "isSupported": item["isSupported"],
            "language": item["language"]
        }
            for item in p["SupportedLanguages"]["SupportedLanguage"]
        ],
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
