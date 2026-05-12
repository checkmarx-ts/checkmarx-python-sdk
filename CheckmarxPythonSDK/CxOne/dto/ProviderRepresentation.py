from dataclasses import dataclass


@dataclass
class ProviderRepresentation:
    operational_info: ... = None
    order: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProviderRepresentation":
        return cls(
            operational_info=item.get("operationalInfo"),
            order=item.get("order"),
        )
