from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.ComponentRepresentation import ComponentRepresentation
from .dto.ComponentTypeRepresentation import ComponentTypeRepresentation
from .api_url import api_url


class ComponentApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{api_client.configuration.iam_base_url.rstrip('/')}{api_url}"

    def get_components(
        self, realm: str, name: str = None, parent: str = None, type: str = None
    ) -> List[ComponentRepresentation]:
        """

        Args:
            realm (str):  [required]
            name (str):
            parent (str):
            type (str):

        Returns:
            List[ComponentRepresentation]

        URL:
            Relative path: /{realm}/components
        """
        params = {"name": name, "parent": parent, "type": type}
        url = f"{self.base_url}/{realm}/components"
        response = self.api_client.call_api("GET", url, params=params)
        return [ComponentRepresentation.from_dict(item) for item in response.json()]

    def post_components(
        self, realm: str, component_representation: ComponentRepresentation
    ) -> bool:
        """

        Args:
            realm (str):  [required]
            component_representation (ComponentRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/components
        """
        url = f"{self.base_url}/{realm}/components"
        response = self.api_client.call_api("POST", url,
            json=component_representation.to_dict(),
            )
        return response.status_code == 204

    def get_component(self, realm: str, id: str) -> ComponentRepresentation:
        """

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            ComponentRepresentation

        URL:
            Relative path: /{realm}/components/{id}
        """
        url = f"{self.base_url}/{realm}/components/{id}"
        response = self.api_client.call_api("GET", url)
        return ComponentRepresentation.from_dict(response.json())

    def put_component(
        self, realm: str, id: str, component_representation: ComponentRepresentation
    ) -> bool:
        """

        Args:
            realm (str):  [required]
            id (str):  [required]
            component_representation (ComponentRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/components/{id}
        """
        url = f"{self.base_url}/{realm}/components/{id}"
        response = self.api_client.call_api("PUT", url,
            json=component_representation.to_dict(),
            )
        return response.status_code == 204

    def delete_component(self, realm: str, id: str) -> bool:
        """

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/components/{id}
        """
        url = f"{self.base_url}/{realm}/components/{id}"
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == 204

    def get_sub_component_types(
        self, realm: str, id: str, type: str = None
    ) -> List[ComponentTypeRepresentation]:
        """
        List of subcomponent types that are available to configure for a particular parent component.

        Args:
            realm (str):  [required]
            id (str):  [required]
            type (str):

        Returns:
            List[ComponentTypeRepresentation]

        URL:
            Relative path: /{realm}/components/{id}/sub-component-types
        """
        params = {"type": type}
        url = f"{self.base_url}/{realm}/components/{id}/sub-component-types"
        response = self.api_client.call_api("GET", url, params=params)
        return [ComponentTypeRepresentation.from_dict(item) for item in response.json()]
