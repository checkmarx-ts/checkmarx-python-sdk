from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne.dto import (
    WebHookInput,
    WebHook, construct_web_hook,
    WebHooksCollection, construct_web_hooks_collection
)
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT

api_url = "/api/webhooks"


class WebHookAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_a_webhook_for_a_tenant(self, webhook_input: WebHookInput) -> WebHook:
        """

        Args:
            webhook_input (WebHookInput):

        Returns:
            WebHook
        """
        relative_url = f"{api_url}/tenant"
        response = self.api_client.post_request(relative_url=relative_url, json=webhook_input.to_dict())
        item = response.json()
        return construct_web_hook(item)

    def get_a_list_of_webhooks_related_to_tenant(self, offset: int = 0, limit: int = 10) -> WebHooksCollection:
        """

        Returns:
            WebHooksCollection
        """
        relative_url = f"{api_url}/tenant"
        params = {"offset": offset, "limit": limit}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return construct_web_hooks_collection(item)

    def create_a_webhook_on_project(self, project_id: str, webhook_input: WebHookInput) -> WebHook:
        """

        Args:
            project_id (str):
            webhook_input (WebHookInput):

        Returns:
            WebHook
        """
        relative_url = f"{api_url}/projects/{project_id}"
        response = self.api_client.post_request(relative_url=relative_url, json=webhook_input.to_dict())
        item = response.json()
        return construct_web_hook(item)

    def get_a_list_of_webhooks_related_to_project(
            self, project_id: str, offset: int = 0, limit: int = 10
    ) -> WebHooksCollection:
        """

        Args:
            project_id (str):
            offset (int):
            limit (int):

        Returns:
          WebHooksCollection
        """

        relative_url = f"{api_url}/projects/{project_id}"
        params = {"offset": offset, "limit": limit}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return construct_web_hooks_collection(item)

    def get_webhook_by_id(self, webhook_id: str) -> WebHook:
        """

        Args:
           webhook_id (str):

        Returns:
            WebHook
        """
        relative_url = f"{api_url}/{webhook_id}"
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_web_hook(item)

    def update_webhook_by_id(self, webhook_id: str, webhook_input: WebHookInput) -> bool:
        """

        Args:
            webhook_id (str):
            webhook_input (WebHookInput):

        Returns:
            bool
        """

        relative_url = f"{api_url}/{webhook_id}"
        response = self.api_client.patch_request(relative_url=relative_url, json=webhook_input.to_dict())
        return response.status_code == NO_CONTENT

    def delete_webhook_by_id(self, webhook_id: str) -> bool:
        """

        Args:
            webhook_id (str):

        Returns:
            bool
        """

        relative_url = f"{api_url}/{webhook_id}"
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT
