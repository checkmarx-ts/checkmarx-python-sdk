# encoding: utf-8
from dataclasses import dataclass, asdict
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED
from .dto import (
    Application,
    ApplicationInput,
    ApplicationsCollection,
    CreatedApplication,
    Rule,
    RuleInput,
)
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List, Optional


class ApplicationsAPI(object):
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/applications"
        )

    def create_an_application(
        self, application_input: ApplicationInput
    ) -> CreatedApplication:
        """
        Args:
            application_input (`ApplicationInput`):

        Returns:
            `CreatedApplication`
        """
        response = self.api_client.call_api(
            method="POST",
            url=self.base_url,
            json={k: v for k, v in asdict(application_input).items() if v is not None},
        )
        return CreatedApplication.from_dict(response.json())

    def get_a_list_of_applications(
        self,
        offset: int = 0,
        limit: int = 20,
        name: str = None,
        tags_keys: List[str] = None,
        tags_values: List[str] = None,
    ) -> ApplicationsCollection:
        """
        Args:
            offset (int): Number of items to skip. Default: 0
            limit (int): Number of items to return. Default: 20
            name (str): Filter by partial name.
            tags_keys (List[str]): Filter by tag keys (OR).
            tags_values (List[str]): Filter by tag values (OR).

        Returns:
            `ApplicationsCollection`
        """
        params = {
            "offset": offset,
            "limit": limit,
            "name": name,
            "tags-keys": tags_keys,
            "tags-values": tags_values,
        }
        response = self.api_client.call_api(
            method="GET",
            url=self.base_url,
            params=params,
        )
        return ApplicationsCollection.from_dict(response.json())

    def get_application_id_by_name(self, name: str) -> Optional[str]:
        """
        Args:
            name (str): application name

        Returns:
            str
        """
        app_collection = self.get_a_list_of_applications(name=name)
        applications = app_collection.applications
        if applications:
            return applications[0].id
        return None

    def get_all_application_tags(self) -> dict:
        """
        Returns:
            dict
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/tags",
        )
        return response.json()

    def get_an_application_by_id(self, application_id: str) -> Application:
        """
        Args:
            application_id (str):

        Returns:
            `Application`
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/{application_id}",
        )
        return Application.from_dict(response.json())

    def update_an_application(
        self, application_id: str, application_input: ApplicationInput
    ) -> bool:
        """
        Args:
            application_id (str):
            application_input (`ApplicationInput`):

        Returns:
            bool
        """
        response = self.api_client.call_api(
            method="PUT",
            url=f"{self.base_url}/{application_id}",
            json={k: v for k, v in asdict(application_input).items() if v is not None},
        )
        return response.status_code == NO_CONTENT

    def delete_an_application(self, application_id: str) -> bool:
        """
        Args:
            application_id (str):

        Returns:
            bool
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=f"{self.base_url}/{application_id}",
        )
        return response.status_code == NO_CONTENT

    def create_an_application_rule(
        self, application_id: str, rule_input: RuleInput
    ) -> Rule:
        """
        Args:
            application_id (str):
            rule_input (`RuleInput`):

        Returns:
            `Rule`
        """
        response = self.api_client.call_api(
            method="POST",
            url=f"{self.base_url}/{application_id}/project-rules",
            json=asdict(rule_input),
        )
        return Rule.from_dict(response.json())

    def get_a_list_of_rules_for_a_specific_application(
        self, application_id: str
    ) -> List[Rule]:
        """
        Args:
            application_id (str):

        Returns:
            `list` of `Rule`
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/{application_id}/project-rules",
        )
        return [Rule.from_dict(rule) for rule in response.json() or []]

    def get_an_application_rule(self, application_id: str, rule_id: str) -> Rule:
        """
        Args:
            application_id (str):
            rule_id (str):

        Returns:
            `Rule`
        """
        response = self.api_client.call_api(
            method="GET",
            url=f"{self.base_url}/{application_id}/project-rules/{rule_id}",
        )
        return Rule.from_dict(response.json())

    def update_an_application_rule(
        self, application_id: str, rule_id: str, rule_input: RuleInput
    ) -> bool:
        """
        Args:
            application_id (str):
            rule_id (str):
            rule_input (`RuleInput`):

        Returns:
            bool
        """
        response = self.api_client.call_api(
            method="PUT",
            url=f"{self.base_url}/{application_id}/project-rules/{rule_id}",
            json=asdict(rule_input),
        )
        return response.status_code in (NO_CONTENT, CREATED)

    def delete_an_application_rule(self, application_id: str, rule_id: str) -> bool:
        """
        Args:
            application_id (str):
            rule_id (str):

        Returns:
            bool
        """
        response = self.api_client.call_api(
            method="DELETE",
            url=f"{self.base_url}/{application_id}/project-rules/{rule_id}",
        )
        return response.status_code == NO_CONTENT


def create_an_application(application_input: ApplicationInput) -> CreatedApplication:
    return ApplicationsAPI().create_an_application(application_input)


def get_a_list_of_applications(
    offset: int = 0,
    limit: int = 20,
    name: str = None,
    tags_keys: List[str] = None,
    tags_values: List[str] = None,
) -> ApplicationsCollection:
    return ApplicationsAPI().get_a_list_of_applications(
        offset=offset,
        limit=limit,
        name=name,
        tags_keys=tags_keys,
        tags_values=tags_values,
    )


def get_application_id_by_name(name: str) -> str:
    return ApplicationsAPI().get_application_id_by_name(name=name)


def get_all_application_tags() -> dict:
    return ApplicationsAPI().get_all_application_tags()


def get_an_application_by_id(application_id: str) -> Application:
    return ApplicationsAPI().get_an_application_by_id(application_id)


def update_an_application(
    application_id: str, application_input: ApplicationInput
) -> bool:
    return ApplicationsAPI().update_an_application(application_id, application_input)


def delete_an_application(application_id: str) -> bool:
    return ApplicationsAPI().delete_an_application(application_id)


def create_an_application_rule(application_id: str, rule_input: RuleInput) -> Rule:
    return ApplicationsAPI().create_an_application_rule(application_id, rule_input)


def get_a_list_of_rules_for_a_specific_application(application_id: str) -> List[Rule]:
    return ApplicationsAPI().get_a_list_of_rules_for_a_specific_application(
        application_id
    )


def get_an_application_rule(application_id: str, rule_id: str) -> Rule:
    return ApplicationsAPI().get_an_application_rule(application_id, rule_id)


def update_an_application_rule(
    application_id: str, rule_id: str, rule_input: RuleInput
) -> bool:
    return ApplicationsAPI().update_an_application_rule(
        application_id, rule_id, rule_input
    )


def delete_an_application_rule(application_id: str, rule_id: str) -> bool:
    return ApplicationsAPI().delete_an_application_rule(application_id, rule_id)
