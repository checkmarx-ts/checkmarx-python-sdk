from dataclasses import dataclass


@dataclass
class QueryDetails:
    id: str = None
    cwe_id: int = None
    language: str = None
    group: str = None
    query_name: str = None
    severity: str = None
    query_description_id: int = None
    custom: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueryDetails":
        return cls(
            id=item.get("queryID"),
            cwe_id=item.get("cweID"),
            language=item.get("language"),
            group=item.get("group"),
            query_name=item.get("queryName"),
            severity=item.get("severity"),
            query_description_id=item.get("queryDescriptionId"),
            custom=item.get("custom"),
        )
