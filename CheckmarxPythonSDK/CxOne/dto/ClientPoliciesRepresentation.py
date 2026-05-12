from dataclasses import dataclass


@dataclass
class ClientPoliciesRepresentation:
    policies: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientPoliciesRepresentation":
        return cls(
            policies=item.get("policies"),
        )
