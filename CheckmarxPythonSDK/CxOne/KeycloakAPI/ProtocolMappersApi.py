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

    def get_client_scope_protocol_mappers_model(self, realm: str, id1: str, id2: str) -> ProtocolMapperRepresentation:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ProtocolMapperRepresentation.from_dict(response.json())

    def put_client_scope_protocol_mappers_model(self, realm: str, id1: str, id2: str,
                                                protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.put_request(relative_url=relative_url, json=protocol_mapper_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 204

    def delete_client_scope_protocol_mappers_model(self, realm: str, id1: str, id2: str) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_client_scope_protocol_mappers_add_models(self, realm: str, id: str,
                                                      protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/protocol_mappers/add_models"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=protocol_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 201

    def get_client_scope_protocol_mappers_models(self, realm: str, id: str) -> List[ProtocolMapperRepresentation]:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/protocol_mappers/models"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ProtocolMapperRepresentation.from_dict(item) for item in response.json()]

    def post_client_scope_protocol_mappers_models(self, realm: str, id: str,
                                                  protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/protocol_mappers/models"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=protocol_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_client_scope_protocol_mappers_protocol(self, realm: str, id: str, protocol: str) -> List[
        ProtocolMapperRepresentation]:
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
        relative_url = f"{api_url}/{realm}/client_scopes/{id}/protocol_mappers/protocol/{protocol}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ProtocolMapperRepresentation.from_dict(item) for item in response.json()]

    def get_client_template_protocol_mappers_model(self, realm: str, id1: str,
                                                   id2: str) -> ProtocolMapperRepresentation:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ProtocolMapperRepresentation.from_dict(response.json())

    def put_client_template_protocol_mappers_model(self, realm: str, id1: str, id2: str,
                                                   protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.put_request(relative_url=relative_url, json=protocol_mapper_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 204

    def delete_client_template_protocol_mappers_model(self, realm: str, id1: str, id2: str) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_client_template_protocol_mappers_add_models(self, realm: str, id: str,
                                                         protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id}/protocol_mappers/add_models"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=protocol_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 201

    def get_client_template_protocol_mappers_models(self, realm: str, id: str) -> List[ProtocolMapperRepresentation]:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id}/protocol_mappers/models"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ProtocolMapperRepresentation.from_dict(item) for item in response.json()]

    def post_client_template_protocol_mappers_models(self, realm: str, id: str,
                                                     protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id}/protocol_mappers/models"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=protocol_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_client_template_protocol_mappers_protocol(self, realm: str, id: str, protocol: str) -> List[
        ProtocolMapperRepresentation]:
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
        relative_url = f"{api_url}/{realm}/client_templates/{id}/protocol_mappers/protocol/{protocol}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ProtocolMapperRepresentation.from_dict(item) for item in response.json()]

    def get_client_protocol_mappers_model(self, realm: str, id1: str, id2: str) -> ProtocolMapperRepresentation:
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
        relative_url = f"{api_url}/{realm}/clients/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return ProtocolMapperRepresentation.from_dict(response.json())

    def put_client_protocol_mappers_model(self, realm: str, id1: str, id2: str,
                                          protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/clients/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.put_request(relative_url=relative_url, json=protocol_mapper_representation.to_dict(),
                                               is_iam=True)
        return response.status_code == 204

    def delete_client_protocol_mappers_model(self, realm: str, id1: str, id2: str) -> bool:
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
        relative_url = f"{api_url}/{realm}/clients/{id1}/protocol_mappers/models/{id2}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_client_protocol_mappers_add_models(self, realm: str, id: str,
                                                protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/clients/{id}/protocol_mappers/add_models"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=protocol_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 201

    def get_client_protocol_mappers_models(self, realm: str, id: str) -> List[ProtocolMapperRepresentation]:
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
        relative_url = f"{api_url}/{realm}/clients/{id}/protocol_mappers/models"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ProtocolMapperRepresentation.from_dict(item) for item in response.json()]

    def post_client_protocol_mappers_models(self, realm: str, id: str,
                                            protocol_mapper_representation: ProtocolMapperRepresentation) -> bool:
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
        relative_url = f"{api_url}/{realm}/clients/{id}/protocol_mappers/models"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=protocol_mapper_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_client_protocol_mappers_protocol(self, realm: str, id: str, protocol: str) -> List[
        ProtocolMapperRepresentation]:
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
        relative_url = f"{api_url}/{realm}/clients/{id}/protocol_mappers/protocol/{protocol}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [ProtocolMapperRepresentation.from_dict(item) for item in response.json()]
