from dataclasses import dataclass


@dataclass
class QueryBuilderMessage:
    role: str = None
    content: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueryBuilderMessage":
        return cls(role=item.get("role"), content=item.get("content"))
