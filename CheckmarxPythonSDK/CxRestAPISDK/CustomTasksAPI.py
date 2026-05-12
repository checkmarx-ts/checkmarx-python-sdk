from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
from CheckmarxPythonSDK.utilities.compat import OK
from .sast.projects.dto import CxCustomTask


class CustomTasksAPI(object):
    """
    REST API: custom tasks
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = api_client.configuration.server_base_url.rstrip("/")

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
        url = f"{self.base_url}/cxrestapi/customTasks"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxCustomTask.from_dict(item) for item in response.json()]
        return result

    def get_custom_task_id_by_name(self, task_name: str) -> int:
        """

        Args:
            task_name (str):

        Returns:
            int: custom task id
        """
        custom_tasks = self.get_all_custom_tasks()
        a_dict = {item.name: item.id for item in custom_tasks}
        return a_dict.get(task_name)

    def get_custom_task_by_id(
        self, task_id: int, api_version: str = "1.0"
    ) -> CxCustomTask:
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
        url = f"{self.base_url}/cxrestapi/customTasks/{task_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxCustomTask.from_dict(response.json())
        return result

    def get_custom_task_by_name(
        self, task_name: str, api_version: str = "1.0"
    ) -> CxCustomTask:
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
        url = f"{self.base_url}/cxrestapi/customTasks/name/{task_name}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            a_list = response.json()
            if a_list:
                result = CxCustomTask.from_dict(a_list[0])
        return result
