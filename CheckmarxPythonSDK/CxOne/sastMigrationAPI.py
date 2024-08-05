import json
from .httpRequests import get_request, post_request, put_request
from .utilities import get_url_param, type_check
from .dto import ImportItem, ImportItemWithLogs, LogItem
from CheckmarxPythonSDK.utilities.compat import OK, ACCEPTED

api_url = "/api/imports"


def launches_import_from_sast_file(file_name, encryption_key, projects_mapping_file_name):
    """

    Args:
        file_name (str):
        encryption_key (str):
        projects_mapping_file_name (str):

    Returns:
        migration_id (str)
    """
    result = None
    relative_url = api_url + "/"
    data = json.dumps(
        {
            "fileName": file_name,
            "encryptionKey": encryption_key,
            "projectsMappingFileName": projects_mapping_file_name
        }
    )
    response = post_request(relative_url=relative_url, data=data)
    if response.status_code == ACCEPTED:
        response = response.json()
        result = response.get("migrationId")
    return result


def get_list_of_imports():
    """

    Returns:
        list of ImportItem
    """
    result = None
    relative_url = api_url + "/"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = [
            ImportItem(
                migration_id=item.get("id"),
                status=item.get("status"),
                created_at=item.get("created_at")
            ) for item in response
        ]
    return result


def get_info_about_import_by_id(migration_id):
    """

    Args:
        migration_id (str):

    Returns:

    """
    result = None
    relative_url = api_url + f"/{migration_id}"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        response = response.json()
        result = ImportItemWithLogs(
            migration_id=response.get("id"),
            status=response.get("status"),
            created_at=response.get("created_at"),
            logs=[
                LogItem(
                    level=item.get("level"),
                    msg=item.get("msg"),
                    time=item.get("time"),
                    error=item.get("error"),
                    worker=item.get("worker"),
                    raw_log=item.get("raw_log"),
                ) for item in response.get("logs")
            ]
        )
    return result


def download_migration_logs(migration_id):
    """

    Args:
        migration_id (str):

    Returns:

    """
    result = None
    relative_url = api_url + f"/{migration_id}/logs/download"
    response = get_request(relative_url=relative_url)
    if response.status_code == OK:
        result = response
    return result

