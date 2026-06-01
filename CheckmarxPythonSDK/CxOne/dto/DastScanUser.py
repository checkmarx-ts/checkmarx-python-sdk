from dataclasses import dataclass
from .DastUserCredentials import DastUserCredentials


@dataclass
class DastScanUser:
    name: str = None
    credentials: DastUserCredentials = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanUser":
        return cls(
            name=item.get("Name"),
            credentials=DastUserCredentials.from_dict(item["Credentials"]) if item.get("Credentials") else None,
        )
