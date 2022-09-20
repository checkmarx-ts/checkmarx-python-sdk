# encoding: utf-8
from .httpRequests import get_request, post_request, put_request, delete_request
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    Application,
    ApplicationInput,
    ApplicationsCollection,
    CreatedApplication,
    Rule,
    RuleInput,
)


def __construct_application_rules(rules):
    rules = rules or []
    return [
        Rule(
            rule_id=rule.get("id"),
            rule_type=rule.get("type"),
            value=rule.get("value")
        ) for rule in rules
    ]


def __construct_application(app):
    return Application(
        application_id=app.get("id"),
        name=app.get("name"),
        description=app.get("description"),
        criticality=app.get("criticality"),
        rules=__construct_application_rules(app.get("rules")),
        project_ids=app.get("projectIds"),
        created_at=app.get("createdAt"),
        updated_at=app.get("updatedAt"),
        tags=app.get("tags")
    )


def create_an_application(application_input):
    """

    Args:
        application_input (`ApplicationInput`):

    Returns:
        `CreatedApplication`
    """
    type_check(application_input, ApplicationInput)

    relative_url = "/api/applications"
    data = application_input.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return CreatedApplication(
        application_id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        criticality=item.get("criticality"),
        rules=__construct_application_rules(item.get("rules")),
        tags=item.get("tags"),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt")
    )


def get_a_list_of_applications(offset=0, limit=20, name=None, tags_keys=None, tags_values=None):
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
    type_check(offset, int)
    type_check(limit, int)
    type_check(name, str)
    type_check(tags_keys, list)
    type_check(tags_values, list)
    list_member_type_check(tags_keys, str)
    list_member_type_check(tags_values, str)

    relative_url = "/api/applications?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    relative_url += get_url_param("name", name)
    relative_url += get_url_param("tags-keys", tags_keys)
    relative_url += get_url_param("tags-values", tags_values)
    response = get_request(relative_url=relative_url)
    app_collection = response.json()
    return ApplicationsCollection(
        total_count=app_collection.get("totalCount"),
        filtered_total_count=app_collection.get("filteredTotalCount"),
        applications=[
            __construct_application(app) for app in app_collection.get("applications")
        ]
    )


def get_application_id_by_name(name):
    """

    Args:
        name (str): application name

    Returns:

    """
    type_check(name, str)

    application_id = None
    app_collection = get_a_list_of_applications(name=name)
    applications = app_collection.applications
    if applications:
        application_id = applications[0].id
    return application_id


def get_all_application_tags():
    """

    Returns:
        dict
        example: {
          "test": [
            ""
          ],
          "priority": [
            "high",
            "low"
          ]
        }
    """
    relative_url = "/api/applications/tags"
    response = get_request(relative_url=relative_url)
    return response.json()


def get_an_application_by_id(application_id):
    """

    Args:
        application_id (str):

    Returns:
        `Application`
    """
    type_check(application_id, str)

    relative_url = "/api/applications/{id}".format(id=application_id)
    response = get_request(relative_url=relative_url)
    app = response.json()
    return __construct_application(app)


def update_an_application(application_id, application_input):
    """

    Args:
        application_id (str):
        application_input (`ApplicationInput`):

    Returns:
        bool
    """
    type_check(application_id, str)
    type_check(application_input, ApplicationInput)

    is_successful = False
    relative_url = "/api/applications/{id}".format(id=application_id)
    data = application_input.get_post_data()
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def delete_an_application(application_id):
    """

    Args:
        application_id (str):

    Returns:

    """
    type_check(application_id, str)

    is_successful = False
    relative_url = "/api/applications/{id}".format(id=application_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def create_an_application_rule(application_id, rule_input):
    """

    Args:
        application_id (str):
        rule_input(`RuleInput`)

    Returns:
        `Rule`
    """
    type_check(application_id, str)
    type_check(rule_input, RuleInput)

    relative_url = "/api/applications/{id}/project-rules".format(id=application_id)
    type_check(rule_input, RuleInput)
    data = rule_input.get_post_data()
    response = post_request(relative_url=relative_url, data=data)
    rule = response.json()
    return Rule(
        rule_id=rule.get("id"),
        rule_type=rule.get("type"),
        value=rule.get("value")
    )


def get_a_list_of_rules_for_a_specific_application(application_id):
    """

    Args:
        application_id (str):

    Returns:
        `list` of `Rule`
    """
    type_check(application_id, str)

    relative_url = "/api/applications/{id}/project-rules".format(id=application_id)
    response = get_request(relative_url=relative_url)
    rules = response.json()
    return __construct_application_rules(rules)


def get_an_application_rule(application_id, rule_id):
    """

    Args:
        application_id (str):
        rule_id (str):

    Returns:
        `Rule`
    """
    type_check(application_id, str)
    type_check(rule_id, str)

    relative_url = "/api/applications/{id}/project-rules/{rule_id}".format(
        id=application_id, rule_id=rule_id
    )
    response = get_request(relative_url=relative_url)
    rule = response.json()
    return Rule(
        rule_id=rule.get("id"),
        rule_type=rule.get("type"),
        value=rule.get("value")
    )


def update_an_application_rule(application_id, rule_id, rule_input):
    """

    Args:
        application_id (str):
        rule_id (str):
        rule_input (`RuleInput`):

    Returns:
       `Rule`
    """
    type_check(application_id, str)
    type_check(rule_id, str)
    type_check(rule_input, RuleInput)

    is_successful = False
    relative_url = "/api/applications/{id}/project-rules/{rule_id}".format(
        id=application_id, rule_id=rule_id
    )
    data = rule_input.get_post_data()
    response = put_request(relative_url=relative_url, data=data)
    if response.status_code in (NO_CONTENT, CREATED):
        is_successful = True
    return is_successful


def delete_an_application_rule(application_id, rule_id):
    """

    Args:
        application_id (str):
        rule_id (str):

    Returns:
        bool
    """
    type_check(application_id, str)
    type_check(rule_id, str)

    is_successful = False
    relative_url = "/api/applications/{id}/project-rules/{rule_id}".format(
        id=application_id, rule_id=rule_id
    )
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful
