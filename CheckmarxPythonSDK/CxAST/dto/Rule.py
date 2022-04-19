# encoding: utf-8
class Rule(object):
    def __init__(self, rule_id, rule_type, value):
        """

        Args:
            rule_id (str): uuid
            rule_type (str): example: project.tag.key-value.exists  Enum: [ project.id.in,
                    project.id.starts-with, project.id.contains, project.id.regex,
                    project.tag.key.exists, project.tag.value.exists, project.tag.key-value.exists ]
            value (str): example: key;value  value of the rule, correlating to the rule type. key-value,
                    and list of ids, should be separated by semicolon (e.g 'key;value', 'id1;id2').
        """
        self.id = rule_id
        self.type = rule_type
        self.value = value

    def __str__(self):
        return """Rule(id={}, type={}, value={})""".format(
            self.id, self.type, self.value
        )
