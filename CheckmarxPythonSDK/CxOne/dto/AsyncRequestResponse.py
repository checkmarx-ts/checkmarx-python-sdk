from dataclasses import dataclass


@dataclass
class AsyncRequestResponse:
    id: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "AsyncRequestResponse":
        return cls(id=item.get("id"))
