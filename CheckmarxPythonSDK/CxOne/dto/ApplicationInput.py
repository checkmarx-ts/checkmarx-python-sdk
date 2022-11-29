# encoding: utf-8
import json
from .RuleInput import RuleInput
from ..utilities import (type_check, int_range_check, list_member_type_check)


class ApplicationInput(object):
    def __init__(self, name, description=None, criticality=3, rules=None, tags=None):
        """

        Args:
            name (str):
            description (str):
            criticality (int):
            rules (`list` of `RuleInput`):
            tags (dict): example:  {
                "test": "",
                "priority": "high"
              }
        """
        type_check(name, str)
        type_check(description, str)
        type_check(criticality, int)
        type_check(rules, list)
        list_member_type_check(rules, RuleInput)
        type_check(tags, dict)
        int_range_check(criticality, 1, 6)

        self.name = name
        self.description = description
        self.criticality = criticality
        self.rules = rules
        self.tags = tags

    def __str__(self):
        return """ApplicationInput(name={}, description={}, criticality={}, rules={}, tags={})""".format(
            self.name, self.description, self.criticality, self.rules, self.tags
        )

    def get_post_data(self):
        data = {
            "name": self.name
        }
        if self.description:
            data.update({"description": self.description})
        if self.criticality:
            data.update({"criticality": self.criticality})
        if self.rules:
            data.update({"rules": [
                {
                    "type": rule.type,
                    "value": rule.value,
                } for rule in self.rules
            ]
            })
        if self.tags:
            data.update({"tags": self.tags})
        return json.dumps(data)
