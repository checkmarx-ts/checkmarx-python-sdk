from dataclasses import dataclass


@dataclass
class GPTMessage:
    role: str = None
    content: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "GPTMessage":
        return cls(role=item.get("role"), content=item.get("content"))
