from dataclasses import dataclass


@dataclass
class ClientPolicyConditionRepresentation:
    condition: ... = None
    configuration: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientPolicyConditionRepresentation":
        return cls(
            condition=item.get("condition"),
            configuration=item.get("configuration"),
        )
