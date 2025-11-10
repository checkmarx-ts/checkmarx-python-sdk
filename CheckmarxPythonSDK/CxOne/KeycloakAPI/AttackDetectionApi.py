from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .api_url import api_url


class AttackDetectionApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def delete_users(self, realm: str) -> bool:
        """
        Clear any user login failures for all users This can release temporary disabled users
        
        Args:
            realm (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/attack-detection/brute-force/users
        """
        relative_url = f"{api_url}/{realm}/attack_detection/brute_force/users"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204

    def get_brute_force_user(self, realm: str, user_id: str) -> Dict[str, Any]:
        """
        Get status of a username in brute force detection
        
        Args:
            realm (str):  [required]
            user_id (str):  [required]
        
        Returns:
            Dict[str, Any]
        
        URL:
            Relative path: /{realm}/attack-detection/brute-force/users/{userId}
        """
        relative_url = f"{api_url}/{realm}/attack_detection/brute_force/users/{user_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def delete_brute_force_user(self, realm: str, user_id: str) -> bool:
        """
        Clear any user login failures for the user This can release temporary disabled user
        
        Args:
            realm (str):  [required]
            user_id (str):  [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/attack-detection/brute-force/users/{userId}
        """
        relative_url = f"{api_url}/{realm}/attack_detection/brute_force/users/{user_id}"
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == 204
