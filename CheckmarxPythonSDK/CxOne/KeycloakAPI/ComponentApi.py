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

    def get_components(self, realm: str, name: str = None, parent: str = None, type: str = None) -> List[
        ComponentRepresentation]:
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
        relative_url = f"{api_url}/{realm}/components"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [ComponentRepresentation.from_dict(item) for item in response.json()]

    def post_components(self, realm: str, component_representation: ComponentRepresentation) -> bool:
        """
        
        Args:
            realm (str):  [required]
            component_representation (ComponentRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/components
        """
        relative_url = f"{api_url}/{realm}/components"
        response = self.api_client.post_request(relative_url=relative_url, json=component_representation.to_dict(),
                                                is_iam=True)
        return response.status_code == 200

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
        relative_url = f"{api_url}/{realm}/components/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ComponentRepresentation.from_dict(response.json())

    def put_component(self, realm: str, id: str, component_representation: ComponentRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/components/{id}"
        response = self.api_client.put_request(relative_url=relative_url, json=component_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 200

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
        relative_url = f"{api_url}/{realm}/components/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_sub_component_types(self, realm: str, id: str, type: str = None) -> List[ComponentTypeRepresentation]:
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
        relative_url = f"{api_url}/{realm}/components/{id}/sub_component_types"
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        return [ComponentTypeRepresentation.from_dict(item) for item in response.json()]
