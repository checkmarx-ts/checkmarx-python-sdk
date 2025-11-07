class ClientPolicyConditionRepresentation:
    def __init__(self, condition, configuration):
        self.condition = condition
        self.configuration = configuration

    def __str__(self):
        return f"ClientPolicyConditionRepresentation(" \
               f"condition={self.condition} " \
               f"configuration={self.configuration} " \
               f")"

    def to_dict(self):
        return {
            "condition": self.condition,
            "configuration": self.configuration,
        }


def construct_client_policy_condition_representation(item):
    return ClientPolicyConditionRepresentation(
        condition=item.get("condition"),
        configuration=item.get("configuration"),
    )
