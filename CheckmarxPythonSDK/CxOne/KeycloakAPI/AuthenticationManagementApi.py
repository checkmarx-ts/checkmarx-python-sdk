from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.AuthenticationExecutionInfoRepresentation import AuthenticationExecutionInfoRepresentation
from .dto.AuthenticationExecutionRepresentation import AuthenticationExecutionRepresentation
from .dto.AuthenticationFlowRepresentation import AuthenticationFlowRepresentation
from .dto.AuthenticatorConfigInfoRepresentation import AuthenticatorConfigInfoRepresentation
from .dto.AuthenticatorConfigRepresentation import AuthenticatorConfigRepresentation
from .dto.RequiredActionProviderRepresentation import RequiredActionProviderRepresentation
from .api_url import api_url


class AuthenticationManagementApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_authenticator_providers(self, realm: str) -> List[Dict[str, Any]]:
        """
        Get authenticator providers Returns a stream of authenticator providers.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[Dict[str, Any]]
        
        URL:
            Relative path: /{realm}/authentication/authenticator-providers
        """
        relative_url = f"{api_url}/{realm}/authentication/authenticator_providers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_client_authenticator_providers(self, realm: str) -> List[Dict[str, Any]]:
        """
        Get client authenticator providers Returns a stream of client authenticator providers.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[Dict[str, Any]]
        
        URL:
            Relative path: /{realm}/authentication/client-authenticator-providers
        """
        relative_url = f"{api_url}/{realm}/authentication/client_authenticator_providers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def post_authentication_config(self, realm: str,
                                   authenticator_config_representation: AuthenticatorConfigRepresentation) -> bool:
        """
        Create new authenticator configuration
        
        Args:
            realm (str):  [required]
            authenticator_config_representation (AuthenticatorConfigRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/config
        """
        relative_url = f"{api_url}/{realm}/authentication/config"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=authenticator_config_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_config_description(self, realm: str, provider_id: str) -> AuthenticatorConfigInfoRepresentation:
        """
        Get authenticator provider’s configuration description
        
        Args:
            realm (str):  [required]
            provider_id (str):  [required]
        
        Returns:
            AuthenticatorConfigInfoRepresentation
        
        URL:
            Relative path: /{realm}/authentication/config-description/{providerId}
        """
        relative_url = f"{api_url}/{realm}/authentication/config_description/{provider_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return AuthenticatorConfigInfoRepresentation.from_dict(response.json())

    def get_authentication_config(self, realm: str, id: str) -> AuthenticatorConfigRepresentation:
        """
        Get authenticator configuration
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            AuthenticatorConfigRepresentation
        
        URL:
            Relative path: /{realm}/authentication/config/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/config/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return AuthenticatorConfigRepresentation.from_dict(response.json())

    def put_authentication_config(self, realm: str, id: str,
                                  authenticator_config_representation: AuthenticatorConfigRepresentation) -> bool:
        """
        Update authenticator configuration
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            authenticator_config_representation (AuthenticatorConfigRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/config/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/config/{id}"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=authenticator_config_representation.to_dict(), is_iam=True)
        return response.status_code == 204

    def delete_config(self, realm: str, id: str) -> bool:
        """
        Delete authenticator configuration
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/config/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/config/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_executions(self, realm: str,
                        authentication_execution_representation: AuthenticationExecutionRepresentation) -> bool:
        """
        Add new authentication execution
        
        Args:
            realm (str):  [required]
            authentication_execution_representation (AuthenticationExecutionRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/executions
        """
        relative_url = f"{api_url}/{realm}/authentication/executions"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=authentication_execution_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_execution(self, realm: str, execution_id: str) -> bool:
        """
        Get Single Execution
        
        Args:
            realm (str):  [required]
            execution_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/executions/{executionId}
        """
        relative_url = f"{api_url}/{realm}/authentication/executions/{execution_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def delete_execution(self, realm: str, execution_id: str) -> bool:
        """
        Delete execution
        
        Args:
            realm (str):  [required]
            execution_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/executions/{executionId}
        """
        relative_url = f"{api_url}/{realm}/authentication/executions/{execution_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_execution_config(self, realm: str, execution_id: str,
                              authenticator_config_representation: AuthenticatorConfigRepresentation) -> bool:
        """
        Update execution with new configuration
        
        Args:
            realm (str):  [required]
            execution_id (str):  [required]
            authenticator_config_representation (AuthenticatorConfigRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/executions/{executionId}/config
        """
        relative_url = f"{api_url}/{realm}/authentication/executions/{execution_id}/config"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=authenticator_config_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def get_execution_config(self, realm: str, execution_id: str, id: str) -> AuthenticatorConfigRepresentation:
        """
        Get execution’s configuration
        
        Args:
            realm (str):  [required]
            execution_id (str):  [required]
            id (str):  [required]
        
        Returns:
            AuthenticatorConfigRepresentation
        
        URL:
            Relative path: /{realm}/authentication/executions/{executionId}/config/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/executions/{execution_id}/config/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return AuthenticatorConfigRepresentation.from_dict(response.json())

    def post_execution_lower_priority(self, realm: str, execution_id: str) -> bool:
        """
        Lower execution’s priority
        
        Args:
            realm (str):  [required]
            execution_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/executions/{executionId}/lower-priority
        """
        relative_url = f"{api_url}/{realm}/authentication/executions/{execution_id}/lower_priority"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def post_execution_raise_priority(self, realm: str, execution_id: str) -> bool:
        """
        Raise execution’s priority
        
        Args:
            realm (str):  [required]
            execution_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/executions/{executionId}/raise-priority
        """
        relative_url = f"{api_url}/{realm}/authentication/executions/{execution_id}/raise_priority"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def get_flows(self, realm: str) -> List[AuthenticationFlowRepresentation]:
        """
        Get authentication flows Returns a stream of authentication flows.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[AuthenticationFlowRepresentation]
        
        URL:
            Relative path: /{realm}/authentication/flows
        """
        relative_url = f"{api_url}/{realm}/authentication/flows"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [AuthenticationFlowRepresentation.from_dict(item) for item in response.json()]

    def post_flows(self, realm: str, authentication_flow_representation: AuthenticationFlowRepresentation) -> bool:
        """
        Create a new authentication flow
        
        Args:
            realm (str):  [required]
            authentication_flow_representation (AuthenticationFlowRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows
        """
        relative_url = f"{api_url}/{realm}/authentication/flows"
        response = self.api_client.post_request(relative_url=relative_url,
                                                json=authentication_flow_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def post_copy(self, realm: str, flow_alias: str) -> bool:
        """
        Copy existing authentication flow under a new name The new name is given as 'newName' attribute of the passed JSON object
        
        Args:
            realm (str):  [required]
            flow_alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{flowAlias}/copy
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{flow_alias}/copy"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_executions(self, realm: str, flow_alias: str) -> bool:
        """
        Get authentication executions for a flow
        
        Args:
            realm (str):  [required]
            flow_alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{flowAlias}/executions
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{flow_alias}/executions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def put_executions(self, realm: str, flow_alias: str,
                       authentication_execution_info_representation: AuthenticationExecutionInfoRepresentation) -> bool:
        """
        Update authentication executions of a Flow
        
        Args:
            realm (str):  [required]
            flow_alias (str):  [required]
            authentication_execution_info_representation (AuthenticationExecutionInfoRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{flowAlias}/executions
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{flow_alias}/executions"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=authentication_execution_info_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def post_execution(self, realm: str, flow_alias: str) -> bool:
        """
        Add new authentication execution to a flow
        
        Args:
            realm (str):  [required]
            flow_alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{flowAlias}/executions/execution
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{flow_alias}/executions/execution"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def post_flow(self, realm: str, flow_alias: str) -> bool:
        """
        Add new flow with new execution to existing flow
        
        Args:
            realm (str):  [required]
            flow_alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{flowAlias}/executions/flow
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{flow_alias}/executions/flow"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 200

    def get_flow(self, realm: str, id: str) -> AuthenticationFlowRepresentation:
        """
        Get authentication flow for id
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            AuthenticationFlowRepresentation
        
        URL:
            Relative path: /{realm}/authentication/flows/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return AuthenticationFlowRepresentation.from_dict(response.json())

    def put_flow(self, realm: str, id: str,
                 authentication_flow_representation: AuthenticationFlowRepresentation) -> bool:
        """
        Update an authentication flow
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            authentication_flow_representation (AuthenticationFlowRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{id}"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=authentication_flow_representation.to_dict(), is_iam=True)
        return response.status_code == 200

    def delete_flow(self, realm: str, id: str) -> bool:
        """
        Delete an authentication flow
        
        Args:
            realm (str):  [required]
            id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/flows/{id}
        """
        relative_url = f"{api_url}/{realm}/authentication/flows/{id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_form_action_providers(self, realm: str) -> List[Dict[str, Any]]:
        """
        Get form action providers Returns a stream of form action providers.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[Dict[str, Any]]
        
        URL:
            Relative path: /{realm}/authentication/form-action-providers
        """
        relative_url = f"{api_url}/{realm}/authentication/form_action_providers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_form_providers(self, realm: str) -> List[Dict[str, Any]]:
        """
        Get form providers Returns a stream of form providers.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[Dict[str, Any]]
        
        URL:
            Relative path: /{realm}/authentication/form-providers
        """
        relative_url = f"{api_url}/{realm}/authentication/form_providers"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_per_client_config_description(self, realm: str) -> Dict[str, Any]:
        """
        Get configuration descriptions for all clients
        
        Args:
            realm (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/authentication/per-client-config-description
        """
        relative_url = f"{api_url}/{realm}/authentication/per_client_config_description"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def post_register_required_action(self, realm: str) -> bool:
        """
        Register a new required actions
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/register-required-action
        """
        relative_url = f"{api_url}/{realm}/authentication/register_required_action"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def get_required_actions(self, realm: str) -> List[RequiredActionProviderRepresentation]:
        """
        Get required actions Returns a stream of required actions.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[RequiredActionProviderRepresentation]
        
        URL:
            Relative path: /{realm}/authentication/required-actions
        """
        relative_url = f"{api_url}/{realm}/authentication/required_actions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return [RequiredActionProviderRepresentation.from_dict(item) for item in response.json()]

    def get_required_action(self, realm: str, alias: str) -> RequiredActionProviderRepresentation:
        """
        Get required action for alias
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            RequiredActionProviderRepresentation
        
        URL:
            Relative path: /{realm}/authentication/required-actions/{alias}
        """
        relative_url = f"{api_url}/{realm}/authentication/required_actions/{alias}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return RequiredActionProviderRepresentation.from_dict(response.json())

    def put_required_action(self, realm: str, alias: str,
                            required_action_provider_representation: RequiredActionProviderRepresentation) -> bool:
        """
        Update required action
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
            required_action_provider_representation (RequiredActionProviderRepresentation): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/required-actions/{alias}
        """
        relative_url = f"{api_url}/{realm}/authentication/required_actions/{alias}"
        response = self.api_client.put_request(relative_url=relative_url,
                                               json=required_action_provider_representation.to_dict(), is_iam=True)
        return response.status_code == 204

    def delete_required_action(self, realm: str, alias: str) -> bool:
        """
        Delete required action
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/required-actions/{alias}
        """
        relative_url = f"{api_url}/{realm}/authentication/required_actions/{alias}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def post_required_action_lower_priority(self, realm: str, alias: str) -> bool:
        """
        Lower required action’s priority
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/required-actions/{alias}/lower-priority
        """
        relative_url = f"{api_url}/{realm}/authentication/required_actions/{alias}/lower_priority"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def post_required_action_raise_priority(self, realm: str, alias: str) -> bool:
        """
        Raise required action’s priority
        
        Args:
            realm (str):  [required]
            alias (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/authentication/required-actions/{alias}/raise-priority
        """
        relative_url = f"{api_url}/{realm}/authentication/required_actions/{alias}/raise_priority"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 201

    def get_unregistered_required_actions(self, realm: str) -> List[str]:
        """
        Get unregistered required actions Returns a stream of unregistered required actions.
        
        Args:
            realm (str):  [required]
        
        Returns:
            List[str]
        
        URL:
            Relative path: /{realm}/authentication/unregistered-required-actions
        """
        relative_url = f"{api_url}/{realm}/authentication/unregistered_required_actions"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()
