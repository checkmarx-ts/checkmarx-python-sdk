from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT
from .dto import (
    DefaultConfig,
    DefaultConfigOut, construct_default_config_out,
    ScanParameter, construct_scan_parameter,
)

api_url = "/api/configuration"


class ScanConfigurationAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_the_list_of_all_the_parameters_defined_for_the_current_tenant(self) -> List[ScanParameter]:
        """

        Returns:
            List[ScanParameter]
        """
        relative_url = api_url + "/tenant"
        response = self.api_client.get_request(relative_url=relative_url)
        response = response.json()
        return [
            construct_scan_parameter(item) for item in response
        ]

    def define_parameters_in_the_input_list_for_the_current_tenant(self, scan_parameters: List[ScanParameter]) -> bool:
        """

        Args:
            scan_parameters (List[ScanParameter]):

        Returns:
            bool
        """
        type_check(scan_parameters, (list, tuple))
        list_member_type_check(scan_parameters, ScanParameter)
        relative_url = api_url + "/tenant"
        response = self.api_client.patch_request(
            relative_url=relative_url,
            json=[
                scan_parameter.to_dict() for scan_parameter in scan_parameters
            ]
        )
        return response.status_code == NO_CONTENT

    def delete_parameters_for_a_tenant(self, config_keys: str) -> bool:
        """

        Args:
            config_keys (str):

        Returns:
            bool
        """
        relative_url = api_url + "/tenant"
        params = {"config-keys": config_keys}
        response = self.api_client.delete_request(relative_url=relative_url, params=params)
        return response.status_code == NO_CONTENT

    def get_the_list_of_all_the_parameters_for_a_project(self, project_id: str) -> List[ScanParameter]:
        """

       Args:
           project_id (str):

       Returns:
            List[ScanParameter]
       """
        type_check(project_id, str)
        relative_url = api_url + "/project"
        params = {"project-id": project_id}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return [
            construct_scan_parameter(item) for item in response or []
        ]

    def define_parameters_in_the_input_list_for_a_specific_project(
            self, project_id: str, scan_parameters: List[ScanParameter]
    ) -> bool:
        """

        Args:
            project_id (str):
            scan_parameters (list of ScanParameter):

        Returns:
            bool
        """
        type_check(project_id, str)
        relative_url = api_url + "/project"
        params = {"project-id": project_id}
        response = self.api_client.patch_request(
            relative_url=relative_url,
            params=params,
            json=[scan_parameter.to_dict() for scan_parameter in scan_parameters]
        )
        return response.status_code == NO_CONTENT

    def delete_parameters_for_a_specific_project(self, project_id: str, config_keys: str) -> bool:
        """

        Args:
            project_id (str):
            config_keys (str):

        Returns:
            bool
        """
        type_check(project_id, str)
        type_check(config_keys, str)
        relative_url = api_url + "/project"
        params = {"project-id": project_id, "config-keys": config_keys}
        response = self.api_client.delete_request(relative_url=relative_url, params=params)
        return response.status_code == NO_CONTENT

    def get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run(
            self, project_id: str, scan_id: str
    ) -> List[ScanParameter]:
        """

        Args:
            project_id (str):
            scan_id (str):

        Returns:
            List[ScanParameter]
        """

        type_check(project_id, str)
        type_check(scan_id, str)
        relative_url = api_url + "/scan"
        params = {"project-id": project_id, "scan-id": scan_id}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return [
            construct_scan_parameter(item) for item in response or []
        ]

    def get_all_default_configs_for_the_tenant(
            self, name: str = None, exact_match: bool = None, limit: int = 100, offset: int = 0
    ) -> List[DefaultConfigOut]:
        """

       Args:
           name (str, optional): Filter by default config name
           exact_match (bool, optional): Forces the filter query to be an exact match instead
           limit (int): Limits the number of returned results. Default value : 100
           offset (int): Offset from which start returned results. Default value : 0

       Returns:
            List[DefaultConfigOut]
       """
        type_check(name, str)
        type_check(exact_match, bool)
        type_check(limit, int)
        type_check(offset, int)
        relative_url = api_url + "/sast/default-config"
        response = self.api_client.get_request(relative_url=relative_url)
        response = response.json()
        return [
            construct_default_config_out(item) for item in response or []
        ]

    def create_a_default_config_for_the_sast_engine(self, default_config: DefaultConfig) -> bool:
        """

        Args:
            default_config (DefaultConfig):

        Returns:
            bool
        """
        type_check(default_config, DefaultConfig)
        relative_url = api_url + "/sast/default-config"
        response = self.api_client.post_request(relative_url=relative_url, json=default_config.to_dict())
        return response.status_code == NO_CONTENT

    def get_sast_default_config_by_id(self, config_id: str) -> DefaultConfigOut:
        """

        Args:
            config_id (str):

        Returns:
           DefaultConfigOut
        """
        type_check(config_id, str)
        relative_url = api_url + "/sast/default-config/{id}".format(id=config_id)
        response = self.api_client.get_request(relative_url=relative_url)
        item = response.json()
        return construct_default_config_out(item)

    def update_default_config_for_the_sast_engine(self, config_id: str, default_config: DefaultConfig) -> bool:
        """

        Args:
            config_id (str):
            default_config (DefaultConfig):

        Returns:
            bool
        """
        type_check(config_id, str)
        type_check(default_config, DefaultConfig)
        relative_url = api_url + "/sast/default-config/{id}".format(id=config_id)
        response = self.api_client.put_request(relative_url=relative_url, json=default_config.to_dict())
        return response.status_code == NO_CONTENT

    def delete_a_sast_default_config(self, config_id) -> bool:
        """

        Args:
            config_id (str):

        Returns:
            bool
        """
        type_check(config_id, str)
        relative_url = api_url + "/sast/default-config/{id}".format(id=config_id)
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT

    def update_project_repo_url(self, project_id: str, repo_url: str) -> bool:
        """

        Args:
            project_id (str):
            repo_url (str):

        Returns:
            bool
        """
        type_check(project_id, str)
        type_check(repo_url, str)
        relative_url = api_url + "/project"
        params = {"project-id": project_id}
        data = [{
            "key": "scan.handler.git.repository",
            "name": "repository",
            "category": "git",
            "originLevel": "Project",
            "value": repo_url,
            "valuetype": "String",
            "allowOverride": True
        }]
        response = self.api_client.patch_request(relative_url=relative_url, params=params, json=data)
        return response.status_code == NO_CONTENT

    def update_project_token(self, project_id: str, token: str) -> bool:
        """

        Args:
            project_id (str):
            token (str):

        Returns:
            bool
        """
        type_check(project_id, str)
        type_check(token, str)
        relative_url = api_url + "/project"
        params = {"project-id": project_id}
        data = [{
            "key": "scan.handler.git.token",
            "name": "token",
            "category": "git",
            "originLevel": "Project",
            "value": token,
            "valuetype": "Secret",
            "allowOverride": True
        }, ]
        response = self.api_client.patch_request(relative_url=relative_url, params=params, json=data)
        return response.status_code == NO_CONTENT


def get_the_list_of_all_the_parameters_defined_for_the_current_tenant() -> List[ScanParameter]:
    return ScanConfigurationAPI().get_the_list_of_all_the_parameters_defined_for_the_current_tenant()


def define_parameters_in_the_input_list_for_the_current_tenant(scan_parameters: List[ScanParameter]) -> bool:
    return ScanConfigurationAPI().define_parameters_in_the_input_list_for_the_current_tenant(
        scan_parameters=scan_parameters
    )


def delete_parameters_for_a_tenant(config_keys: str) -> bool:
    return ScanConfigurationAPI().delete_parameters_for_a_tenant(config_keys=config_keys)


def get_the_list_of_all_the_parameters_for_a_project(project_id: str) -> List[ScanParameter]:
    return ScanConfigurationAPI().get_the_list_of_all_the_parameters_for_a_project(project_id=project_id)


def define_parameters_in_the_input_list_for_a_specific_project(
        project_id: str, scan_parameters: List[ScanParameter]
) -> bool:
    return ScanConfigurationAPI().define_parameters_in_the_input_list_for_a_specific_project(
        project_id=project_id, scan_parameters=scan_parameters
    )


def delete_parameters_for_a_specific_project(project_id: str, config_keys: str) -> bool:
    return ScanConfigurationAPI().delete_parameters_for_a_specific_project(
        project_id=project_id, config_keys=config_keys
    )


def get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run(
        project_id: str,
        scan_id: str
) -> List[ScanParameter]:
    return ScanConfigurationAPI().get_the_list_of_all_parameters_that_will_be_used_in_the_scan_run(
        project_id=project_id, scan_id=scan_id
    )


def get_all_default_configs_for_the_tenant(
        name: str = None,  # Filter by default config name
        exact_match: bool = None,  # Forces the filter query to be an exact match instead
        limit: int = 100,  # Limits the number of returned results. Default value : 100
        offset: int = 0,  # Offset from which start returned results. Default value : 0
) -> List[DefaultConfigOut]:
    return ScanConfigurationAPI().get_all_default_configs_for_the_tenant(
        name=name, exact_match=exact_match, limit=limit, offset=offset
    )


def create_a_default_config_for_the_sast_engine(default_config: DefaultConfig) -> bool:
    return ScanConfigurationAPI().create_a_default_config_for_the_sast_engine(default_config=default_config)


def get_sast_default_config_by_id(config_id: str) -> DefaultConfigOut:
    return ScanConfigurationAPI().get_sast_default_config_by_id(config_id=config_id)


def update_default_config_for_the_sast_engine(config_id: str, default_config: DefaultConfig) -> bool:
    return ScanConfigurationAPI().update_default_config_for_the_sast_engine(
        config_id=config_id, default_config=default_config
    )


def delete_a_sast_default_config(config_id) -> bool:
    return ScanConfigurationAPI().delete_a_sast_default_config(config_id=config_id)


def update_project_repo_url(project_id: str, repo_url: str) -> bool:
    return ScanConfigurationAPI().update_project_repo_url(project_id=project_id, repo_url=repo_url)


def update_project_token(project_id: str, token: str) -> bool:
    return ScanConfigurationAPI().update_project_token(project_id=project_id, token=token)
