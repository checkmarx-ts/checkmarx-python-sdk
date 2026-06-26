from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List

from .dto import (
    ScaProjectWithConfigurations,
    ScaRegistryConfigRequest,
    ScaRegistryConfigResponse,
    ScaRegistryConfiguration,
    ScaTagWithConfigurations,
)


class ScaPrivateRegistryConfigAPI(object):
    """API client for the SCA Private Registry Configuration Management REST API.

    Enables creating and managing private repository registry configurations,
    and associating them with projects and tags. Private registry
    configurations allow SCA to access private package repositories.

    Base URL: {server}/api/sca/registries-configuration
    """

    _base_path = "/api/sca/registries-configuration"

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = self.api_client.configuration.server_base_url

    # =========================================================================
    # Configuration endpoints
    # =========================================================================

    def get_all_configurations(
        self, page_number: int, page_size: int = 5
    ) -> List[ScaRegistryConfiguration]:
        """Retrieve a list of all private registry configurations associated
        with your tenant account.

        Args:
            page_number (int): Page number to retrieve (required).
            page_size (int): Number of configurations per page. Default: 5.

        Returns:
            List[ScaRegistryConfiguration]: List of configurations.
        """
        url = f"{self.base_url}{self._base_path}/configurations"
        params = {"PageNumber": page_number, "PageSize": page_size}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [
            ScaRegistryConfiguration.from_dict(item) for item in response.json()
        ]

    def create_configuration(
        self, config_request: ScaRegistryConfigRequest
    ) -> ScaRegistryConfigResponse:
        """Create a configuration for accessing a private repository.

        Submitting Configuration Content:
            The request body must contain the configuration content. Use the
            relevant template (NuGet XML, Maven settings.xml, or NPM .npmrc)
            and replace placeholder values with your real credentials.

        Args:
            config_request (ScaRegistryConfigRequest): Configuration properties
                including configurationName, content, and packageManager.

        Returns:
            ScaRegistryConfigResponse: Response containing the id of the
            created configuration and a message.
        """
        url = f"{self.base_url}{self._base_path}/configurations"
        response = self.api_client.call_api(
            method="POST",
            url=url,
            json=config_request.to_dict(),
        )
        return ScaRegistryConfigResponse.from_dict(response.json())

    def get_configuration(self, config_id: str) -> ScaRegistryConfiguration:
        """Retrieve a specific configuration identified by configId.

        Args:
            config_id (str): Unique identifier of the configuration.

        Returns:
            ScaRegistryConfiguration: The configuration details including id,
            configurationName, tenantId, content, tags, packageManager,
            projects, and lastUpdate.
        """
        url = f"{self.base_url}{self._base_path}/configurations/{config_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return ScaRegistryConfiguration.from_dict(response.json())

    def delete_configuration(self, config_id: str) -> bool:
        """Delete a specific configuration identified by configId.

        Args:
            config_id (str): Unique identifier of the configuration.

        Returns:
            bool: True if the deletion was successful.
        """
        url = f"{self.base_url}{self._base_path}/configurations/{config_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == 204

    def update_configuration(
        self, config_id: str, config_request: ScaRegistryConfigRequest
    ) -> bool:
        """Modify the name and content of a particular configuration.

        The request body must contain the configuration content. Use the
        relevant template (NuGet XML, Maven settings.xml, or NPM .npmrc)
        and replace placeholder values with your real credentials.

        Args:
            config_id (str): Unique identifier of the configuration.
            config_request (ScaRegistryConfigRequest): Updated configuration
                properties including configurationName, content, and
                packageManager.

        Returns:
            bool: True if the update was successful.
        """
        url = f"{self.base_url}{self._base_path}/configurations/{config_id}"
        response = self.api_client.call_api(
            method="PATCH",
            url=url,
            json=config_request.to_dict(),
        )
        return response.status_code == 200

    def get_project_configurations(
        self, project_id: str
    ) -> List[ScaRegistryConfiguration]:
        """Retrieve all configurations associated with a particular Checkmarx
        project.

        Args:
            project_id (str): Unique identifier of the project.

        Returns:
            List[ScaRegistryConfiguration]: List of configurations associated
            with the project.
        """
        url = f"{self.base_url}{self._base_path}/configurations/project/{project_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            ScaRegistryConfiguration.from_dict(item)
            for item in response.json()
        ]

    def associate_configurations_with_project(
        self, project_id: str, config_ids: List[str]
    ) -> ScaRegistryConfigResponse:
        """Associate one or more existing private repository configurations
        with a particular Checkmarx project.

        Args:
            project_id (str): Unique identifier of the project.
            config_ids (List[str]): List of configuration IDs to associate.

        Returns:
            ScaRegistryConfigResponse: Response containing the association id
            and a message.
        """
        url = f"{self.base_url}{self._base_path}/configurations/project/{project_id}"
        response = self.api_client.call_api(
            method="POST", url=url, json=config_ids
        )
        return ScaRegistryConfigResponse.from_dict(response.json())

    def disassociate_configurations_from_project(
        self, project_id: str, config_ids: List[str] = None
    ) -> bool:
        """Disassociate private repo configurations from a particular Checkmarx
        project. This does not delete the configurations; it merely
        disassociates them from this project.

        Args:
            project_id (str): Unique identifier of the project.
            config_ids (List[str]): List of configuration IDs to disassociate.
                If omitted, disassociates all configurations from the project.

        Returns:
            bool: True if disassociation was successful.
        """
        url = f"{self.base_url}{self._base_path}/configurations/project/{project_id}"
        params = None
        if config_ids:
            params = {"configurationIds": config_ids}
        response = self.api_client.call_api(
            method="DELETE", url=url, params=params
        )
        return response.status_code == 204

    def get_configurations_by_tag(
        self, tag_id: str
    ) -> List[ScaTagWithConfigurations]:
        """Retrieve a list of configurations associated with a specific tag.

        Args:
            tag_id (str): Unique identifier of the tag.

        Returns:
            List[ScaTagWithConfigurations]: List of tags with their associated
            configurations. Each item contains the tag id, tenantId, name,
            and a list of configurations.
        """
        url = f"{self.base_url}{self._base_path}/configurations/tag/{tag_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            ScaTagWithConfigurations.from_dict(item)
            for item in response.json()
        ]

    def associate_configurations_with_tag(
        self, tag_id: str, config_ids: List[str]
    ) -> ScaRegistryConfigResponse:
        """Associate one or more existing private repository configurations
        with a particular tag.

        Args:
            tag_id (str): Unique identifier of the tag.
            config_ids (List[str]): List of configuration IDs to associate.

        Returns:
            ScaRegistryConfigResponse: Response containing the association id
            and a message.
        """
        url = f"{self.base_url}{self._base_path}/configurations/tag/{tag_id}"
        response = self.api_client.call_api(
            method="POST", url=url, json=config_ids
        )
        return ScaRegistryConfigResponse.from_dict(response.json())

    def disassociate_configurations_from_tag(self, tag_id: str) -> bool:
        """Disassociate all private repo configurations from a particular tag.

        Args:
            tag_id (str): Unique identifier of the tag.

        Returns:
            bool: True if disassociation was successful.
        """
        url = f"{self.base_url}{self._base_path}/configurations/tag/{tag_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == 204

    # =========================================================================
    # Project endpoints
    # =========================================================================

    def get_projects_with_configurations(
        self, page_number: int, page_size: int = 5
    ) -> List[ScaProjectWithConfigurations]:
        """Retrieve a list of Checkmarx projects with their associated private
        registries configurations.

        Args:
            page_number (int): Page number to retrieve (required).
            page_size (int): Number of results per page. Default: 5.

        Returns:
            List[ScaProjectWithConfigurations]: List of projects with their
            associated configurations.
        """
        url = f"{self.base_url}{self._base_path}/projects"
        params = {"PageNumber": page_number, "PageSize": page_size}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [
            ScaProjectWithConfigurations.from_dict(item)
            for item in response.json()
        ]

    def get_projects_by_configuration(
        self, config_id: str
    ) -> List[ScaProjectWithConfigurations]:
        """Retrieve a list of Checkmarx projects associated with a particular
        configuration.

        Filters at the project level — only projects associated with the
        requested configId are returned. Within those projects, you may see
        other configurations also associated with that same project.

        Args:
            config_id (str): Unique identifier of the configuration.

        Returns:
            List[ScaProjectWithConfigurations]: List of projects associated
            with the configuration.
        """
        url = f"{self.base_url}{self._base_path}/projects/configuration/{config_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return [
            ScaProjectWithConfigurations.from_dict(item)
            for item in response.json()
        ]

    def disassociate_all_projects_from_configuration(
        self, config_id: str
    ) -> bool:
        """Disassociate all Checkmarx projects from a particular configuration.

        Args:
            config_id (str): Unique identifier of the configuration.

        Returns:
            bool: True if disassociation was successful.
        """
        url = f"{self.base_url}{self._base_path}/projects/configuration/{config_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == 204

    def associate_projects_with_configuration(
        self, config_id: str, project_ids: List[str]
    ) -> ScaRegistryConfigResponse:
        """Associate one or more Checkmarx projects with a particular private
        repository configuration.

        Args:
            config_id (str): Unique identifier of the configuration.
            project_ids (List[str]): List of project IDs to associate.

        Returns:
            ScaRegistryConfigResponse: Response containing the association id
            and a message.
        """
        url = f"{self.base_url}{self._base_path}/projects/configuration/{config_id}"
        response = self.api_client.call_api(
            method="POST", url=url, json=project_ids
        )
        return ScaRegistryConfigResponse.from_dict(response.json())

    # =========================================================================
    # Tag endpoints
    # =========================================================================

    def get_tags_with_configurations(self) -> dict:
        """Retrieve a list of tags with their associated private registries
        configurations.

        Returns:
            dict: List of tags with their associated configurations.
        """
        url = f"{self.base_url}{self._base_path}/tags"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def create_tag(self, tag_data: dict) -> dict:
        """Create a new tag.

        Args:
            tag_data (dict): Tag properties including name.

        Returns:
            dict: The created tag.
        """
        url = f"{self.base_url}{self._base_path}/tags"
        response = self.api_client.call_api(
            method="POST", url=url, json=tag_data
        )
        return response.json()

    def get_tag(self, tag_id: str) -> dict:
        """Retrieve a particular tag with its details.

        Args:
            tag_id (str): Unique identifier of the tag.

        Returns:
            dict: The tag details.
        """
        url = f"{self.base_url}{self._base_path}/tags/{tag_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def update_tag(self, tag_id: str, update_data: dict) -> dict:
        """Change the name of an existing tag.

        Args:
            tag_id (str): Unique identifier of the tag.
            update_data (dict): Fields to update (e.g. name).

        Returns:
            dict: The updated tag.
        """
        url = f"{self.base_url}{self._base_path}/tags/{tag_id}"
        response = self.api_client.call_api(
            method="PATCH", url=url, json=update_data
        )
        return response.json()

    def delete_tag(self, tag_id: str) -> bool:
        """Delete a particular tag.

        Args:
            tag_id (str): Unique identifier of the tag.

        Returns:
            bool: True if deletion was successful.
        """
        url = f"{self.base_url}{self._base_path}/tags/{tag_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == 204

    def get_tags_by_configuration(self, config_id: str) -> dict:
        """Retrieve a list of all tags associated with a particular
        configuration.

        Args:
            config_id (str): Unique identifier of the configuration.

        Returns:
            dict: List of tags associated with the configuration.
        """
        url = f"{self.base_url}{self._base_path}/tags/configuration/{config_id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def associate_tags_with_configuration(
        self, config_id: str, tag_ids: List[str]
    ) -> dict:
        """Associate one or more tags with a particular private repository
        configuration.

        Args:
            config_id (str): Unique identifier of the configuration.
            tag_ids (List[str]): List of tag IDs to associate.

        Returns:
            dict: Response indicating the association result.
        """
        url = f"{self.base_url}{self._base_path}/tags/configuration/{config_id}"
        response = self.api_client.call_api(
            method="POST", url=url, json={"tagIds": tag_ids}
        )
        return response.json()

    def disassociate_all_tags_from_configuration(
        self, config_id: str
    ) -> bool:
        """Disassociate all tags from a particular configuration.

        Args:
            config_id (str): Unique identifier of the configuration.

        Returns:
            bool: True if disassociation was successful.
        """
        url = f"{self.base_url}{self._base_path}/tags/configuration/{config_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == 204


# =============================================================================
# Standalone functions
# =============================================================================


def get_all_configurations(
    page_number: int, page_size: int = 5
) -> List[ScaRegistryConfiguration]:
    """Retrieve a list of all private registry configurations associated with
    your tenant account.

    Args:
        page_number (int): Page number to retrieve (required).
        page_size (int): Number of configurations per page. Default: 5.

    Returns:
        List[ScaRegistryConfiguration]: List of configurations.
    """
    return ScaPrivateRegistryConfigAPI().get_all_configurations(
        page_number, page_size
    )


def create_configuration(
    config_request: ScaRegistryConfigRequest,
) -> ScaRegistryConfigResponse:
    """Create a configuration for accessing a private repository.

    Submitting Configuration Content:
        The request body must contain the configuration content. Use the
        relevant template (NuGet XML, Maven settings.xml, or NPM .npmrc)
        and replace placeholder values with your real credentials.

    Args:
        config_request (ScaRegistryConfigRequest): Configuration properties
            including configurationName, content, and packageManager.

    Returns:
        ScaRegistryConfigResponse: Response containing the id of the created
        configuration and a message.
    """
    return ScaPrivateRegistryConfigAPI().create_configuration(config_request)


def get_configuration(config_id: str) -> ScaRegistryConfiguration:
    """Retrieve a specific configuration identified by configId.

    Args:
        config_id (str): Unique identifier of the configuration.

    Returns:
        ScaRegistryConfiguration: The configuration details including id,
        configurationName, tenantId, content, tags, packageManager, projects,
        and lastUpdate.
    """
    return ScaPrivateRegistryConfigAPI().get_configuration(config_id)


def delete_configuration(config_id: str) -> bool:
    """Delete a specific configuration identified by configId.

    Args:
        config_id (str): Unique identifier of the configuration.

    Returns:
        bool: True if the deletion was successful.
    """
    return ScaPrivateRegistryConfigAPI().delete_configuration(config_id)


def update_configuration(
    config_id: str, config_request: ScaRegistryConfigRequest
) -> bool:
    """Modify the name and content of a particular configuration.

    The request body must contain the configuration content. Use the relevant
    template (NuGet XML, Maven settings.xml, or NPM .npmrc) and replace
    placeholder values with your real credentials.

    Args:
        config_id (str): Unique identifier of the configuration.
        config_request (ScaRegistryConfigRequest): Updated configuration
            properties including configurationName, content, and
            packageManager.

    Returns:
        bool: True if the update was successful.
    """
    return ScaPrivateRegistryConfigAPI().update_configuration(
        config_id, config_request
    )


def get_project_configurations(
    project_id: str,
) -> List[ScaRegistryConfiguration]:
    """Retrieve all configurations associated with a particular Checkmarx
    project.

    Args:
        project_id (str): Unique identifier of the project.

    Returns:
        List[ScaRegistryConfiguration]: List of configurations associated with
        the project.
    """
    return ScaPrivateRegistryConfigAPI().get_project_configurations(project_id)


def associate_configurations_with_project(
    project_id: str, config_ids: List[str]
) -> ScaRegistryConfigResponse:
    """Associate one or more existing private repository configurations with a
    particular Checkmarx project.

    Args:
        project_id (str): Unique identifier of the project.
        config_ids (List[str]): List of configuration IDs to associate.

    Returns:
        ScaRegistryConfigResponse: Response containing the association id and
        a message.
    """
    return ScaPrivateRegistryConfigAPI().associate_configurations_with_project(
        project_id, config_ids
    )


def disassociate_configurations_from_project(
    project_id: str, config_ids: List[str] = None
) -> bool:
    """Disassociate private repo configurations from a particular Checkmarx
    project. This does not delete the configurations; it merely disassociates
    them from this project.

    Args:
        project_id (str): Unique identifier of the project.
        config_ids (List[str]): List of configuration IDs to disassociate.
            If omitted, disassociates all configurations from the project.

    Returns:
        bool: True if disassociation was successful.
    """
    return (
        ScaPrivateRegistryConfigAPI().disassociate_configurations_from_project(
            project_id, config_ids
        )
    )


def get_configurations_by_tag(
    tag_id: str,
) -> List[ScaTagWithConfigurations]:
    """Retrieve a list of configurations associated with a specific tag.

    Args:
        tag_id (str): Unique identifier of the tag.

    Returns:
        List[ScaTagWithConfigurations]: List of tags with their associated
        configurations. Each item contains the tag id, tenantId, name, and a
        list of configurations.
    """
    return ScaPrivateRegistryConfigAPI().get_configurations_by_tag(tag_id)


def associate_configurations_with_tag(
    tag_id: str, config_ids: List[str]
) -> ScaRegistryConfigResponse:
    """Associate one or more existing private repository configurations with a
    particular tag.

    Args:
        tag_id (str): Unique identifier of the tag.
        config_ids (List[str]): List of configuration IDs to associate.

    Returns:
        ScaRegistryConfigResponse: Response containing the association id and
        a message.
    """
    return ScaPrivateRegistryConfigAPI().associate_configurations_with_tag(
        tag_id, config_ids
    )


def disassociate_configurations_from_tag(tag_id: str) -> bool:
    """Disassociate all private repo configurations from a particular tag.

    Args:
        tag_id (str): Unique identifier of the tag.

    Returns:
        bool: True if disassociation was successful.
    """
    return (
        ScaPrivateRegistryConfigAPI().disassociate_configurations_from_tag(
            tag_id
        )
    )


def get_projects_with_configurations(
    page_number: int, page_size: int = 5
) -> List[ScaProjectWithConfigurations]:
    """Retrieve a list of Checkmarx projects with their associated private
    registries configurations.

    Args:
        page_number (int): Page number to retrieve (required).
        page_size (int): Number of results per page. Default: 5.

    Returns:
        List[ScaProjectWithConfigurations]: List of projects with their
        associated configurations.
    """
    return ScaPrivateRegistryConfigAPI().get_projects_with_configurations(
        page_number, page_size
    )


def get_projects_by_configuration(
    config_id: str,
) -> List[ScaProjectWithConfigurations]:
    """Retrieve a list of Checkmarx projects associated with a particular
    configuration.

    Filters at the project level — only projects associated with the requested
    configId are returned. Within those projects, you may see other
    configurations also associated with that same project.

    Args:
        config_id (str): Unique identifier of the configuration.

    Returns:
        List[ScaProjectWithConfigurations]: List of projects associated with
        the configuration.
    """
    return ScaPrivateRegistryConfigAPI().get_projects_by_configuration(
        config_id
    )


def disassociate_all_projects_from_configuration(config_id: str) -> bool:
    """Disassociate all Checkmarx projects from a particular configuration.

    Args:
        config_id (str): Unique identifier of the configuration.

    Returns:
        bool: True if disassociation was successful.
    """
    return (
        ScaPrivateRegistryConfigAPI().disassociate_all_projects_from_configuration(
            config_id
        )
    )


def associate_projects_with_configuration(
    config_id: str, project_ids: List[str]
) -> ScaRegistryConfigResponse:
    """Associate one or more Checkmarx projects with a particular private
    repository configuration.

    Args:
        config_id (str): Unique identifier of the configuration.
        project_ids (List[str]): List of project IDs to associate.

    Returns:
        ScaRegistryConfigResponse: Response containing the association id and
        a message.
    """
    return ScaPrivateRegistryConfigAPI().associate_projects_with_configuration(
        config_id, project_ids
    )


def get_tags_with_configurations() -> dict:
    """Retrieve a list of tags with their associated private registries
    configurations.

    Returns:
        dict: List of tags with their associated configurations.
    """
    return ScaPrivateRegistryConfigAPI().get_tags_with_configurations()


def create_tag(tag_data: dict) -> dict:
    """Create a new tag.

    Args:
        tag_data (dict): Tag properties including name.

    Returns:
        dict: The created tag.
    """
    return ScaPrivateRegistryConfigAPI().create_tag(tag_data)


def get_tag(tag_id: str) -> dict:
    """Retrieve a particular tag with its details.

    Args:
        tag_id (str): Unique identifier of the tag.

    Returns:
        dict: The tag details.
    """
    return ScaPrivateRegistryConfigAPI().get_tag(tag_id)


def update_tag(tag_id: str, update_data: dict) -> dict:
    """Change the name of an existing tag.

    Args:
        tag_id (str): Unique identifier of the tag.
        update_data (dict): Fields to update (e.g. name).

    Returns:
        dict: The updated tag.
    """
    return ScaPrivateRegistryConfigAPI().update_tag(tag_id, update_data)


def delete_tag(tag_id: str) -> bool:
    """Delete a particular tag.

    Args:
        tag_id (str): Unique identifier of the tag.

    Returns:
        bool: True if deletion was successful.
    """
    return ScaPrivateRegistryConfigAPI().delete_tag(tag_id)


def get_tags_by_configuration(config_id: str) -> dict:
    """Retrieve a list of all tags associated with a particular configuration.

    Args:
        config_id (str): Unique identifier of the configuration.

    Returns:
        dict: List of tags associated with the configuration.
    """
    return ScaPrivateRegistryConfigAPI().get_tags_by_configuration(config_id)


def associate_tags_with_configuration(
    config_id: str, tag_ids: List[str]
) -> dict:
    """Associate one or more tags with a particular private repository
    configuration.

    Args:
        config_id (str): Unique identifier of the configuration.
        tag_ids (List[str]): List of tag IDs to associate.

    Returns:
        dict: Response indicating the association result.
    """
    return ScaPrivateRegistryConfigAPI().associate_tags_with_configuration(
        config_id, tag_ids
    )


def disassociate_all_tags_from_configuration(config_id: str) -> bool:
    """Disassociate all tags from a particular configuration.

    Args:
        config_id (str): Unique identifier of the configuration.

    Returns:
        bool: True if disassociation was successful.
    """
    return (
        ScaPrivateRegistryConfigAPI().disassociate_all_tags_from_configuration(
            config_id
        )
    )
