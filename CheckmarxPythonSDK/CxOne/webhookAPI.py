from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne.dto import (
    WebHookInput,
    WebHook,
    WebHooksCollection,
)
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT


class WebHookAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/webhooks"
        )

    def create_a_webhook_for_a_tenant(
        self, webhook_input: WebHookInput
    ) -> WebHook:
        """
        Create a webhook for a tenant.

        Args:
            webhook_input (WebHookInput):

        Returns:
            WebHook
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/tenant",
            json=asdict(webhook_input),
        )
        return WebHook.from_dict(response.json())

    def get_a_list_of_webhooks_related_to_tenant(
        self, offset: int = 0, limit: int = 10
    ) -> WebHooksCollection:
        """
        Get a list of webhooks related to a tenant.

        Args:
            offset (int):
            limit (int):

        Returns:
            WebHooksCollection
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/tenant",
            params={"offset": offset, "limit": limit},
        )
        return WebHooksCollection.from_dict(response.json())

    def create_a_webhook_on_project(
        self, project_id: str, webhook_input: WebHookInput
    ) -> WebHook:
        """
        Create a webhook on a project.

        Args:
            project_id (str):
            webhook_input (WebHookInput):

        Returns:
            WebHook
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/projects/{project_id}",
            json=asdict(webhook_input),
        )
        return WebHook.from_dict(response.json())

    def get_a_list_of_webhooks_related_to_project(
        self, project_id: str, offset: int = 0, limit: int = 10
    ) -> WebHooksCollection:
        """
        Get a list of webhooks related to a project.

        Args:
            project_id (str):
            offset (int):
            limit (int):

        Returns:
            WebHooksCollection
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/projects/{project_id}",
            params={"offset": offset, "limit": limit},
        )
        return WebHooksCollection.from_dict(response.json())

    def get_webhook_by_id(self, webhook_id: str) -> WebHook:
        """
        Get a webhook by ID.

        Args:
            webhook_id (str):

        Returns:
            WebHook
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/{webhook_id}",
        )
        return WebHook.from_dict(response.json())

    def update_webhook_by_id(
        self, webhook_id: str, webhook_input: WebHookInput
    ) -> bool:
        """
        Update a webhook by ID.

        Args:
            webhook_id (str):
            webhook_input (WebHookInput):

        Returns:
            bool
        """
        response = self.api_client.call_api(
            method="PATCH",
            url=f"{self.base_url}/{webhook_id}",
            json=asdict(webhook_input),
        )
        return response.status_code == NO_CONTENT

    def delete_webhook_by_id(self, webhook_id: str) -> bool:
        """
        Delete a webhook by ID.

        Args:
            webhook_id (str):

        Returns:
            bool
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=f"{self.base_url}/{webhook_id}",
        )
        return response.status_code == NO_CONTENT
