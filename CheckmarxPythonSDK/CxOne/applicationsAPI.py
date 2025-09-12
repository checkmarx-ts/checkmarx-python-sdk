# encoding: utf-8
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED
from .utilities import type_check
from .dto import (
    Application, construct_application_rules, construct_application,
    ApplicationInput,
    ApplicationsCollection,
    CreatedApplication,
    Rule,
    RuleInput,
)
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List

api_url = "/api/applications"


class ApplicationsAPI(object):
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def create_an_application(self, application_input: ApplicationInput) -> CreatedApplication:
        """

       Args:
           application_input (`ApplicationInput`):

       Returns:
           `CreatedApplication`
       """
        type_check(application_input, ApplicationInput)
        relative_url = api_url
        response = self.api_client.post_request(relative_url=relative_url, json=application_input.to_dict())
        item = response.json()
        return CreatedApplication(
            application_id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            criticality=item.get("criticality"),
            rules=construct_application_rules(item.get("rules")),
            tags=item.get("tags"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt")
        )

    def get_a_list_of_applications(
            self, offset: int = 0, limit: int = 20, name: str = None, tags_keys: List[str] = None,
            tags_values: List[str] = None
    ) -> ApplicationsCollection:
        """

        Args:
           offset (int): The number of items to skip before starting to collect the result set
                       Default value : 0
           limit (int):  The number of items to return
                       Default value : 20
           name (str): Application name, can be filtered by partial name.
           tags_keys (`list` of `str`): Application tags, filter by the keys in the tags map
                                   (OR operation between the items)
           tags_values (`list` of `str`): Application tags, filter by the values in the tags map
                                   (OR operation between the items)

       Returns:
           `ApplicationsCollection`
       """
        relative_url = api_url
        params = {"offset": offset, "limit": limit, "name": name, "tags-keys": tags_keys, "tags-values": tags_values}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        app_collection = response.json()
        return ApplicationsCollection(
            total_count=app_collection.get("totalCount"),
            filtered_total_count=app_collection.get("filteredTotalCount"),
            applications=[
                construct_application(app) for app in app_collection.get("applications")
            ]
        )

    def get_application_id_by_name(self, name: str) -> str:
        """

        Args:
            name (str): application name

        Returns:

        """
        type_check(name, str)
        application_id = None
        app_collection = self.get_a_list_of_applications(name=name)
        applications = app_collection.applications
        if applications:
            application_id = applications[0].application_id
        return application_id

    def get_all_application_tags(self) -> dict:
        """

        Returns:
            dict
            example: {
              "test": [],
              "priority": [
                "high",
                "low"
              ]
            }
        """
        relative_url = api_url + "/tags"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json()

    def get_an_application_by_id(self, application_id: str) -> Application:
        """

        Args:
            application_id (str):

        Returns:
            `Application`
        """
        type_check(application_id, str)
        relative_url = api_url + "/{id}".format(id=application_id)
        response = self.api_client.get_request(relative_url=relative_url)
        app = response.json()
        return construct_application(app)

    def update_an_application(self, application_id: str, application_input: ApplicationInput) -> bool:
        """

        Args:
            application_id (str):
            application_input (`ApplicationInput`):

        Returns:
            bool
        """
        type_check(application_id, str)
        type_check(application_input, ApplicationInput)
        relative_url = api_url + "/{id}".format(id=application_id)
        response = self.api_client.put_request(relative_url=relative_url, json=application_input.to_dict())
        return response.status_code == NO_CONTENT

    def delete_an_application(self, application_id: str) -> bool:
        """

        Args:
            application_id (str):

        Returns:
            bool
        """
        type_check(application_id, str)

        relative_url = api_url + "/{id}".format(id=application_id)
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT

    def create_an_application_rule(self, application_id: str, rule_input: RuleInput) -> Rule:
        """

        Args:
            application_id (str):
            rule_input(`RuleInput`)

        Returns:
            `Rule`
        """
        type_check(application_id, str)
        type_check(rule_input, RuleInput)
        relative_url = api_url + "/{id}/project-rules".format(id=application_id)
        type_check(rule_input, RuleInput)
        response = self.api_client.post_request(relative_url=relative_url, json=rule_input.to_dict())
        rule = response.json()
        return Rule(
            rule_id=rule.get("id"),
            rule_type=rule.get("type"),
            value=rule.get("value")
        )

    def get_a_list_of_rules_for_a_specific_application(self, application_id: str) -> List[Rule]:
        """

        Args:
            application_id (str):

        Returns:
            `list` of `Rule`
        """
        type_check(application_id, str)
        relative_url = api_url + "/{id}/project-rules".format(id=application_id)
        response = self.api_client.get_request(relative_url=relative_url)
        rules = response.json()
        return construct_application_rules(rules)

    def get_an_application_rule(self, application_id: str, rule_id: str) -> Rule:
        """

        Args:
            application_id (str):
            rule_id (str):

        Returns:
            `Rule`
        """
        type_check(application_id, str)
        type_check(rule_id, str)
        relative_url = api_url + "/{id}/project-rules/{rule_id}".format(
            id=application_id, rule_id=rule_id
        )
        response = self.api_client.get_request(relative_url=relative_url)
        rule = response.json()
        return Rule(
            rule_id=rule.get("id"),
            rule_type=rule.get("type"),
            value=rule.get("value")
        )

    def update_an_application_rule(self, application_id: str, rule_id: str, rule_input: RuleInput) -> bool:
        """

        Args:
            application_id (str):
            rule_id (str):
            rule_input (`RuleInput`):

        Returns:
           bool
        """
        type_check(application_id, str)
        type_check(rule_id, str)
        type_check(rule_input, RuleInput)
        is_successful = False
        relative_url = api_url + "/{id}/project-rules/{rule_id}".format(
            id=application_id, rule_id=rule_id
        )
        response = self.api_client.put_request(relative_url=relative_url, json=rule_input.to_dict())
        if response.status_code in (NO_CONTENT, CREATED):
            is_successful = True
        return is_successful

    def delete_an_application_rule(self, application_id: str, rule_id: str) -> bool:
        """

        Args:
            application_id (str):
            rule_id (str):

        Returns:
            bool
        """
        type_check(application_id, str)
        type_check(rule_id, str)
        relative_url = api_url + "/{id}/project-rules/{rule_id}".format(
            id=application_id, rule_id=rule_id
        )
        response = self.api_client.delete_request(relative_url=relative_url)
        return response.status_code == NO_CONTENT


def create_an_application(application_input: ApplicationInput) -> CreatedApplication:
    return ApplicationsAPI().create_an_application(application_input)


def get_a_list_of_applications(
        offset: int = 0, limit: int = 20, name: str = None, tags_keys: List[str] = None, tags_values: List[str] = None
) -> ApplicationsCollection:
    return ApplicationsAPI().get_a_list_of_applications(
        offset=offset, limit=limit, name=name, tags_keys=tags_keys, tags_values=tags_values
    )


def get_application_id_by_name(name: str) -> str:
    return ApplicationsAPI().get_application_id_by_name(name=name)


def get_all_application_tags() -> dict:
    return ApplicationsAPI().get_all_application_tags()


def get_an_application_by_id(application_id: str) -> Application:
    return ApplicationsAPI().get_an_application_by_id(application_id)


def update_an_application(application_id: str, application_input: ApplicationInput) -> bool:
    return ApplicationsAPI().update_an_application(application_id, application_input)


def delete_an_application(application_id: str) -> bool:
    return ApplicationsAPI().delete_an_application(application_id)


def create_an_application_rule(application_id: str, rule_input: RuleInput) -> Rule:
    return ApplicationsAPI().create_an_application_rule(application_id, rule_input)


def get_a_list_of_rules_for_a_specific_application(application_id: str) -> List[Rule]:
    return ApplicationsAPI().get_a_list_of_rules_for_a_specific_application(application_id)


def get_an_application_rule(application_id: str, rule_id: str) -> Rule:
    return ApplicationsAPI().get_an_application_rule(application_id, rule_id)


def update_an_application_rule(application_id: str, rule_id: str, rule_input: RuleInput) -> bool:
    return ApplicationsAPI().update_an_application_rule(application_id, rule_id, rule_input)


def delete_an_application_rule(application_id: str, rule_id: str) -> bool:
    return ApplicationsAPI().delete_an_application_rule(application_id, rule_id)
