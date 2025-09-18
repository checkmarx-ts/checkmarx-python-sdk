from dataclasses import dataclass


@dataclass
class RuleInput:
    """

    Attributes:
        type (str): example: project.tag.key-value.exists  Enum: [ project.id.in,
                project.id.starts-with, project.id.contains, project.id.regex,
                project.tag.key.exists, project.tag.value.exists, project.tag.key-value.exists ]
        value (str): example: key;value  value of the rule, correlating to the rule type. key-value,
                and list of ids, should be separated by semicolon (e.g 'key;value', 'id1;id2').
    """
    type: str
    value: str

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
        }
