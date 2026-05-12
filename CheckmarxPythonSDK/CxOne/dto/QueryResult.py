from dataclasses import dataclass


@dataclass
class QueryResult:
    content: str = None
    line_number: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueryResult":
        return cls(
            content=item.get("content"),
            line_number=item.get("lineNumber"),
        )
