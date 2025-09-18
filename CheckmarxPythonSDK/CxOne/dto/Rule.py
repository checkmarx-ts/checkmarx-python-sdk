from dataclasses import dataclass


@dataclass
class Rule:
    """

    Attributes:
        id (str): uuid
        type (str): example: project.tag.key-value.exists  Enum: [ project.id.in,
                project.id.starts-with, project.id.contains, project.id.regex,
                project.tag.key.exists, project.tag.value.exists, project.tag.key-value.exists ]
        value (str): example: key;value  value of the rule, correlating to the rule type. key-value,
                and list of ids, should be separated by semicolon (e.g 'key;value', 'id1;id2').
    """
    id: str
    type: str
    value: str


def construct_rule(item):
    return Rule(
        id=item.get("id"),
        type=item.get("type"),
        value=item.get("value")
    )
