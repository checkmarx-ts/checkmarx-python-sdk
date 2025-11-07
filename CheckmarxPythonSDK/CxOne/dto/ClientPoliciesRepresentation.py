class ClientPoliciesRepresentation:
    def __init__(self, policies):
        self.policies = policies

    def __str__(self):
        return f"ClientPoliciesRepresentation(" \
               f"policies={self.policies} " \
               f")"

    def to_dict(self):
        return {
            "policies": self.policies,
        }


def construct_client_policies_representation(item):
    return ClientPoliciesRepresentation(
        policies=item.get("policies"),
    )
