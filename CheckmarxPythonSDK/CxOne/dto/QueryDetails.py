from dataclasses import dataclass


@dataclass
class QueryDetails:
    """

    Attributes:
        id (str):
        cwe_id (int):
        language (str):
        group (str):
        query_name (str):
        severity (str):
        query_description_id (int):
        custom (bool):
    """
    id: str
    cwe_id: int
    language: str
    group: str
    query_name: str
    severity: str
    query_description_id: int
    custom: bool


def construct_query_details(item):
    return QueryDetails(
        id=item.get("id"),
        cwe_id=item.get("cweID"),
        language=item.get("language"),
        group=item.get("group"),
        query_name=item.get("queryName"),
        severity=item.get("severity"),
        query_description_id=item.get("queryDescriptionId"),
        custom=item.get("custom")
    )
