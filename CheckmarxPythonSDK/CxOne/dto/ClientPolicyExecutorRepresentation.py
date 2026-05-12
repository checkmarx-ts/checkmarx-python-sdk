from dataclasses import dataclass


@dataclass
class ClientPolicyExecutorRepresentation:
    configuration: ... = None
    executor: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientPolicyExecutorRepresentation":
        return cls(
            configuration=item.get("configuration"),
            executor=item.get("executor"),
        )
