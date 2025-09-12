from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.projects.dto import CxCustomTask
from .sast.projects.dto import CxLink


class CustomTasksAPI(object):
    """
    REST API: custom tasks
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_custom_tasks(self, api_version: str = "1.0") -> List[CxCustomTask]:
        """
        REST API: get all custom tasks

        Args:
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxCustomTask`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        result = []
        relative_url = "/cxrestapi/customTasks"
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_list = response.json()
            result = [
                CxCustomTask(
                    custom_task_id=item.get("id"),
                    name=item.get("name"),
                    custom_task_type=item.get("type"),
                    data=item.get("data"),
                    link=CxLink(
                        (item.get("link", {}) or {}).get("rel"),
                        (item.get("link", {}) or {}).get("uri")
                    )
                ) for item in a_list
            ]
        return result

    def get_custom_task_id_by_name(self, task_name: str) -> int:
        """

        Args:
            task_name (str):

        Returns:
            int: custom task id
        """
        custom_tasks = self.get_all_custom_tasks()
        a_dict = {
            item.name: item.id for item in custom_tasks
        }
        return a_dict.get(task_name)

    def get_custom_task_by_id(self, task_id: int, api_version: str = "1.0") -> CxCustomTask:
        """

        Args:
            task_id (int):  Unique Id of the custom task
            api_version (str, optional):

        Returns:
            :obj:`CxCustomTask`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/customTasks/{id}".format(id=task_id)
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxCustomTask(
                custom_task_id=a_dict.get("id"),
                name=a_dict.get("name"),
                custom_task_type=a_dict.get("type"),
                data=a_dict.get("data"),
                link=CxLink(
                    (a_dict.get("link", {}) or {}).get("rel"),
                    (a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    def get_custom_task_by_name(self, task_name: str, api_version: str = "1.0") -> CxCustomTask:
        """

        Args:
            task_name (str):
            api_version (str, optional):

        Returns:
            :obj:`CxCustomTask`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/customTasks/name/{name}".format(name=task_name)
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_list = response.json()
            if a_list:
                a_dict = a_list[0]
                result = CxCustomTask(
                    custom_task_id=a_dict.get("id"),
                    name=a_dict.get("name"),
                    custom_task_type=a_dict.get("type"),
                    data=a_dict.get("data"),
                    link=CxLink(
                        (a_dict.get("link", {}) or {}).get("rel"),
                        (a_dict.get("link", {}) or {}).get("uri")
                    )
                )
        return result
