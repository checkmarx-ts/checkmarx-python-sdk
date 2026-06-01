from dataclasses import dataclass


@dataclass
class DastApplication:
    application_id: str = None
    is_primary: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastApplication":
        return cls(
            application_id=item.get("applicationId"),
            is_primary=item.get("isPrimary"),
        )
