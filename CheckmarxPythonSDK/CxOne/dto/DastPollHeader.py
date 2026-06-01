from dataclasses import dataclass


@dataclass
class DastPollHeader:
    header: str = None
    value: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastPollHeader":
        return cls(
            header=item.get("header"),
            value=item.get("value"),
        )
