from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.ProtocolMapperRepresentation import ProtocolMapperRepresentation
from .api_url import api_url


class ProtocolMappersApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{api_client.configuration.iam_base_url.rstrip('/')}{api_url}"

    def get_client_scope_protocol_mappers_model(
        self, realm: str, id1: str, id2: str
    ) -> ProtocolMapperRepresentation:
        """
        Get mapper by id

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]

        Returns:
            ProtocolMapperRepresentation

        URL:
            Relative path: /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("GET", url)
        return ProtocolMapperRepresentation.from_dict(response.json())

    def put_client_scope_protocol_mappers_model(
        self,
        realm: str,
        id1: str,
        id2: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Update the mapper

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("PUT", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 204

    def delete_client_scope_protocol_mappers_model(
        self, realm: str, id1: str, id2: str
    ) -> bool:
        """
        Delete the mapper

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == 204

    def post_client_scope_protocol_mappers_add_models(
        self,
        realm: str,
        id: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Create multiple mappers

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-scopes/{id}/protocol-mappers/add-models
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id}/protocol-mappers/add-models"
        response = self.api_client.call_api("POST", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 201

    def get_client_scope_protocol_mappers_models(
        self, realm: str, id: str
    ) -> List[ProtocolMapperRepresentation]:
        """
        Get mappers

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[ProtocolMapperRepresentation]

        URL:
            Relative path: /{realm}/client-scopes/{id}/protocol-mappers/models
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id}/protocol-mappers/models"
        response = self.api_client.call_api("GET", url)
        return [
            ProtocolMapperRepresentation.from_dict(item) for item in response.json()
        ]

    def post_client_scope_protocol_mappers_models(
        self,
        realm: str,
        id: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Create a mapper

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-scopes/{id}/protocol-mappers/models
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id}/protocol-mappers/models"
        response = self.api_client.call_api("POST", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 200

    def get_client_scope_protocol_mappers_protocol(
        self, realm: str, id: str, protocol: str
    ) -> List[ProtocolMapperRepresentation]:
        """
        Get mappers by name for a specific protocol

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol (str):  [required]

        Returns:
            List[ProtocolMapperRepresentation]

        URL:
            Relative path: /{realm}/client-scopes/{id}/protocol-mappers/protocol/{protocol}
        """
        url = f"{self.base_url}/{realm}/client-scopes/{id}/protocol-mappers/protocol/{protocol}"
        response = self.api_client.call_api("GET", url)
        return [
            ProtocolMapperRepresentation.from_dict(item) for item in response.json()
        ]

    def get_client_template_protocol_mappers_model(
        self, realm: str, id1: str, id2: str
    ) -> ProtocolMapperRepresentation:
        """
        Get mapper by id

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]

        Returns:
            ProtocolMapperRepresentation

        URL:
            Relative path: /{realm}/client-templates/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/client-templates/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("GET", url)
        return ProtocolMapperRepresentation.from_dict(response.json())

    def put_client_template_protocol_mappers_model(
        self,
        realm: str,
        id1: str,
        id2: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Update the mapper

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-templates/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/client-templates/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("PUT", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 204

    def delete_client_template_protocol_mappers_model(
        self, realm: str, id1: str, id2: str
    ) -> bool:
        """
        Delete the mapper

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-templates/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/client-templates/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == 204

    def post_client_template_protocol_mappers_add_models(
        self,
        realm: str,
        id: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Create multiple mappers

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-templates/{id}/protocol-mappers/add-models
        """
        url = f"{self.base_url}/{realm}/client-templates/{id}/protocol-mappers/add-models"
        response = self.api_client.call_api("POST", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 201

    def get_client_template_protocol_mappers_models(
        self, realm: str, id: str
    ) -> List[ProtocolMapperRepresentation]:
        """
        Get mappers

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[ProtocolMapperRepresentation]

        URL:
            Relative path: /{realm}/client-templates/{id}/protocol-mappers/models
        """
        url = f"{self.base_url}/{realm}/client-templates/{id}/protocol-mappers/models"
        response = self.api_client.call_api("GET", url)
        return [
            ProtocolMapperRepresentation.from_dict(item) for item in response.json()
        ]

    def post_client_template_protocol_mappers_models(
        self,
        realm: str,
        id: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Create a mapper

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/client-templates/{id}/protocol-mappers/models
        """
        url = f"{self.base_url}/{realm}/client-templates/{id}/protocol-mappers/models"
        response = self.api_client.call_api("POST", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 200

    def get_client_template_protocol_mappers_protocol(
        self, realm: str, id: str, protocol: str
    ) -> List[ProtocolMapperRepresentation]:
        """
        Get mappers by name for a specific protocol

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol (str):  [required]

        Returns:
            List[ProtocolMapperRepresentation]

        URL:
            Relative path: /{realm}/client-templates/{id}/protocol-mappers/protocol/{protocol}
        """
        url = f"{self.base_url}/{realm}/client-templates/{id}/protocol-mappers/protocol/{protocol}"
        response = self.api_client.call_api("GET", url)
        return [
            ProtocolMapperRepresentation.from_dict(item) for item in response.json()
        ]

    def get_client_protocol_mappers_model(
        self, realm: str, id1: str, id2: str
    ) -> ProtocolMapperRepresentation:
        """
        Get mapper by id

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]

        Returns:
            ProtocolMapperRepresentation

        URL:
            Relative path: /{realm}/clients/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/clients/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("GET", url)
        return ProtocolMapperRepresentation.from_dict(response.json())

    def put_client_protocol_mappers_model(
        self,
        realm: str,
        id1: str,
        id2: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Update the mapper

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/clients/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/clients/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("PUT", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 204

    def delete_client_protocol_mappers_model(
        self, realm: str, id1: str, id2: str
    ) -> bool:
        """
        Delete the mapper

        Args:
            realm (str):  [required]
            id1 (str):  [required]
            id2 (str):  [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/clients/{id1}/protocol-mappers/models/{id2}
        """
        url = f"{self.base_url}/{realm}/clients/{id1}/protocol-mappers/models/{id2}"
        response = self.api_client.call_api("DELETE", url)
        return response.status_code == 204

    def post_client_protocol_mappers_add_models(
        self,
        realm: str,
        id: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Create multiple mappers

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/clients/{id}/protocol-mappers/add-models
        """
        url = f"{self.base_url}/{realm}/clients/{id}/protocol-mappers/add-models"
        response = self.api_client.call_api("POST", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 201

    def get_client_protocol_mappers_models(
        self, realm: str, id: str
    ) -> List[ProtocolMapperRepresentation]:
        """
        Get mappers

        Args:
            realm (str):  [required]
            id (str):  [required]

        Returns:
            List[ProtocolMapperRepresentation]

        URL:
            Relative path: /{realm}/clients/{id}/protocol-mappers/models
        """
        url = f"{self.base_url}/{realm}/clients/{id}/protocol-mappers/models"
        response = self.api_client.call_api("GET", url)
        return [
            ProtocolMapperRepresentation.from_dict(item) for item in response.json()
        ]

    def post_client_protocol_mappers_models(
        self,
        realm: str,
        id: str,
        protocol_mapper_representation: ProtocolMapperRepresentation,
    ) -> bool:
        """
        Create a mapper

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol_mapper_representation (ProtocolMapperRepresentation): Request body data [required]

        Returns:
            bool

        URL:
            Relative path: /{realm}/clients/{id}/protocol-mappers/models
        """
        url = f"{self.base_url}/{realm}/clients/{id}/protocol-mappers/models"
        response = self.api_client.call_api("POST", url,
            json=protocol_mapper_representation.to_dict(),
            )
        return response.status_code == 200

    def get_client_protocol_mappers_protocol(
        self, realm: str, id: str, protocol: str
    ) -> List[ProtocolMapperRepresentation]:
        """
        Get mappers by name for a specific protocol

        Args:
            realm (str):  [required]
            id (str):  [required]
            protocol (str):  [required]

        Returns:
            List[ProtocolMapperRepresentation]

        URL:
            Relative path: /{realm}/clients/{id}/protocol-mappers/protocol/{protocol}
        """
        url = f"{self.base_url}/{realm}/clients/{id}/protocol-mappers/protocol/{protocol}"
        response = self.api_client.call_api("GET", url)
        return [
            ProtocolMapperRepresentation.from_dict(item) for item in response.json()
        ]
