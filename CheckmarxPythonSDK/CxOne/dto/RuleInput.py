# encoding: utf-8
import json
from ..utilities import (type_check)


class RuleInput(object):
    def __init__(self, rule_type, value):
        """

        Args:
            rule_type (str): example: project.tag.key-value.exists  Enum: [ project.id.in,
                    project.id.starts-with, project.id.contains, project.id.regex,
                    project.tag.key.exists, project.tag.value.exists, project.tag.key-value.exists ]
            value (str): example: key;value  value of the rule, correlating to the rule type. key-value,
                    and list of ids, should be separated by semicolon (e.g 'key;value', 'id1;id2').
        """
        if rule_type not in [
            "project.name.starts-with", "project.name.in", "project.name.contains", "project.name.regex",
            "project.id.in", "project.id.starts-with", "project.id.contains", "project.id.regex",
            "project.tag.key.exists", "project.tag.value.exists", "project.tag.key-value.exists",

        ]:
            raise ValueError("""Error for parameter rule_type, must be one of [ project.id.in,
                    project.id.starts-with, project.id.contains, project.id.regex,
                    project.tag.key.exists, project.tag.value.exists, project.tag.key-value.exists ] """)
        type_check(rule_type, str)
        type_check(value, str)
        self.type = rule_type
        self.value = value

    def __str__(self):
        return """RuleInput(type={type}, value={value})""".format(
            type=self.type, value=self.value
        )

    def get_post_data(self):
        return json.dumps(
            {
                "type": self.type,
                "value": self.value,
            }
        )
