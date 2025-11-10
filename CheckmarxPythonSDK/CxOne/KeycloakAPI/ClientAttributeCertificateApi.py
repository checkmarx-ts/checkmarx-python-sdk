from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import Dict, List, Any, Optional
from .dto.CertificateRepresentation import CertificateRepresentation
from .dto.KeyStoreConfig import KeyStoreConfig
from .api_url import api_url


class ClientAttributeCertificateApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_certificate(self, realm: str, id: str, attr: str) -> CertificateRepresentation:
        """
        Get key info
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            attr (str):  [required]
        
        Returns:
            CertificateRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/certificates/{attr}
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/certificates/{attr}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return CertificateRepresentation.from_dict(response.json())

    def post_download(self, realm: str, id: str, attr: str, key_store_config: KeyStoreConfig) -> bool:
        """
        Get a keystore file for the client, containing private key and public certificate
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            attr (str):  [required]
            key_store_config (KeyStoreConfig): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/certificates/{attr}/download
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/certificates/{attr}/download"
        response = self.api_client.post_request(relative_url=relative_url, json=key_store_config.to_dict(), is_iam=True)
        return response.status_code == 200

    def post_generate(self, realm: str, id: str, attr: str) -> CertificateRepresentation:
        """
        Generate a new certificate with new key pair
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            attr (str):  [required]
        
        Returns:
            CertificateRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/certificates/{attr}/generate
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/certificates/{attr}/generate"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return CertificateRepresentation.from_dict(response.json())

    def post_generate_and_download(self, realm: str, id: str, attr: str, key_store_config: KeyStoreConfig) -> bool:
        """
        Generate a new keypair and certificate, and get the private key file  Generates a keypair and certificate and serves the private key in a specified keystore format. Only generated public certificate is saved in Keycloak DB - the private key is not.
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            attr (str):  [required]
            key_store_config (KeyStoreConfig): Request body data [required]
        
        Returns:
            bool
        
        URL:
            Relative path: /{realm}/clients/{id}/certificates/{attr}/generate-and-download
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/certificates/{attr}/generate_and_download"
        response = self.api_client.post_request(relative_url=relative_url, json=key_store_config.to_dict(), is_iam=True)
        return response.status_code == 200

    def post_upload(self, realm: str, id: str, attr: str) -> CertificateRepresentation:
        """
        Upload certificate and eventually private key
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            attr (str):  [required]
        
        Returns:
            CertificateRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/certificates/{attr}/upload
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/certificates/{attr}/upload"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return CertificateRepresentation.from_dict(response.json())

    def post_upload_certificate(self, realm: str, id: str, attr: str) -> CertificateRepresentation:
        """
        Upload only certificate, not private key
        
        Args:
            realm (str):  [required]
            id (str):  [required]
            attr (str):  [required]
        
        Returns:
            CertificateRepresentation
        
        URL:
            Relative path: /{realm}/clients/{id}/certificates/{attr}/upload-certificate
        """
        relative_url = f"{api_url}/{realm}/clients/{id}/certificates/{attr}/upload_certificate"
        response = self.api_client.post_request(relative_url=relative_url, is_iam=True)
        return CertificateRepresentation.from_dict(response.json())
