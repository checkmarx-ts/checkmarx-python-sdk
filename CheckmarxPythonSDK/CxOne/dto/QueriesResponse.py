from dataclasses import dataclass


@dataclass
class QueriesResponse:
    name: str = None
    is_active: bool = None
    last_modified: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueriesResponse":
        return cls(
            name=item.get("name"),
            is_active=item.get("isActive"),
            last_modified=item.get("lastModified"),
        )
