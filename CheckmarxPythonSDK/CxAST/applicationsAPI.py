# encoding: utf-8
import json

from .httpRequests import get_request, post_request, put_request, delete_request
from ..compat import NO_CONTENT, CREATED


def create_an_application(name, description=None, criticality=None, rules=None, tags=None):
    """

    Args:
        name (str):
        description (str):
        criticality (int):
        rules (`list` of `dict`): example: [
            {
              "type": "project.tag.key-value.exists",
              "value": "key;value"
            }
          ]
        tags (dict): example:  {
            "test": "",
            "priority": "high"
          }

    Returns:
        dict
        example: {
          "id": "string",
          "name": "string",
          "description": "string",
          "criticality": 3,
          "rules": [
            {
              "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "type": "project.tag.key-value.exists",
              "value": "key;value"
            }
          ],
          "tags": {
            "test": "",
            "priority": "high"
          },
          "createdAt": "2022-03-02T06:37:14.128Z",
          "updatedAt": "2022-03-02T06:37:14.128Z"
        }
    """
    relative_url = "/api/applications"
    data = {
        "name": name
    }
    if description:
        data.update({"description": description})
    if criticality:
        data.update({"criticality": criticality})
    if rules and isinstance(rules, (list, tuple)):
        data.update({"rules": [
                {
                    "type": rule.get("type"),
                    "value": rule.get("value"),
                } for rule in rules
            ]
        })
    if tags:
        data.update({"tags": tags})
    data = json.dumps(data)
    response = post_request(relative_url=relative_url, data=data)
    return response.json()


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
        dict
        example:  {
              "totalCount": 0,
              "filteredTotalCount": 0,
              "applications": [
                {
                  "id": "string",
                  "name": "string",
                  "description": "string",
                  "criticality": 3,
                  "rules": [
                    {
                      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                      "type": "project.tag.key-value.exists",
                      "value": "key;value"
                    }
                  ],
                  "projectIds": [
                    "string"
                  ],
                  "createdAt": "2022-03-02T06:58:12.355Z",
                  "updatedAt": "2022-03-02T06:58:12.355Z",
                  "tags": {
                    "test": "",
                    "priority": "high"
                  }
                }
              ]
            }
    """
    relative_url = "/api/applications?offset={offset}&limit={offset}".format(offset=offset, limit=limit)
    if name:
        relative_url += "&name={name}".format(name=name)
    if tags_keys and isinstance(tags_keys, (list, tuple)):
        for tags_key in tags_keys:
            relative_url += "&tags-keys={tags_key}".format(tags_key=tags_key)
    if tags_values and isinstance(tags_values, (list, tuple)):
        for tags_value in tags_values:
            relative_url += "&tags-values={tags_value}".format(tags_value=tags_value)

    response = get_request(relative_url=relative_url)
    return response.json()


def get_application_id_by_name(name):
    """

    Args:
        name (str): application name

    Returns:

    """
    application_id = None
    response = get_a_list_of_applications(name=name)
    applications = response.get("applications")
    if applications:
        application_id = applications[0].get("id")
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
        dict
        example: {
          "id": "string",
          "name": "string",
          "description": "string",
          "criticality": 3,
          "rules": [
            {
              "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "type": "project.tag.key-value.exists",
              "value": "key;value"
            }
          ],
          "projectIds": [
            "string"
          ],
          "createdAt": "2022-03-02T07:33:23.184Z",
          "updatedAt": "2022-03-02T07:33:23.184Z",
          "tags": {
            "test": "",
            "priority": "high"
          }
        }
    """
    relative_url = "/api/applications/{id}".format(id=application_id)
    response = get_request(relative_url=relative_url)
    return response.json()


def update_an_application(application_id, name=None, description=None, criticality=None, rules=None, tags=None):
    """

    Args:
        application_id (str):
        name (str):
        description (str):
        criticality (str):
        rules (`list` of `dict`):
        tags (dict):

    Returns:
        bool
    """
    is_successful = False
    relative_url = "/api/applications/{id}".format(id=application_id)
    data = {}
    if name:
        data.update({"name": name})
    if description:
        data.update({"description": description})
    if criticality:
        data.update({"criticality": criticality})
    if rules:
        data.update({"rules": rules})
    if tags:
        data.update({"tags": tags})
    data = json.dumps(data)
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
    is_successful = False
    relative_url = "/api/applications/{id}".format(id=application_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def create_an_application_rule(application_id, rule_type, rule_value):
    """

    Args:
        application_id (str):
        rule_type (str): "project.tag.key-value.exists"
        rule_value (str): "key;value"

    Returns:
        dict
            example: {
              "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "type": "project.tag.key-value.exists",
              "value": "key;value"
            }
    """
    relative_url = "/api/applications/{id}/project-rules".format(id=application_id)
    data = {
      "type": rule_type,
      "value": rule_value,
    }
    data = json.dumps(data)
    response = post_request(relative_url=relative_url, data=data)
    return response.json()


def get_a_list_of_rules_for_a_specific_application(application_id):
    """

    Args:
        application_id (str):

    Returns:
        `list` of `dict`
        example: [
          {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "type": "project.tag.key-value.exists",
            "value": "key;value"
          }
        ]
    """
    relative_url = "/api/applications/{id}/project-rules".format(id=application_id)
    response = get_request(relative_url=relative_url)
    return response.json()


def get_an_application_rule(application_id, rule_id):
    """

    Args:
        application_id (str):
        rule_id (str):

    Returns:
        dict
        example: {
                  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  "type": "project.tag.key-value.exists",
                  "value": "key;value"
                }
    """
    relative_url = "/api/applications/{id}/project-rules/{rule_id}".format(id=application_id, rule_id=rule_id)
    response = get_request(relative_url=relative_url)
    return response.json()


def update_an_application_rule(application_id, rule_id, rule_type, rule_value):
    """

    Args:
        application_id (str):
        rule_id (str):
        rule_type (str):
        rule_value (str):

    Returns:
        dict
        example: {
                  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  "type": "project.tag.key-value.exists",
                  "value": "key;value"
                }
    """
    is_successful = False
    relative_url = "/api/applications/{id}/project-rules/{rule_id}".format(id=application_id, rule_id=rule_id)
    data = json.dumps(
        {
            "type": rule_type,
            "value": rule_value
        }
    )
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
    is_successful = False
    relative_url = "/api/applications/{id}/project-rules/{rule_id}".format(id=application_id, rule_id=rule_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful
