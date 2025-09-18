from dataclasses import dataclass


@dataclass
class Query:
    """

    Attributes:
        id (int):
        source (str):
        level (str):
        path (str):
        modified (str):
        cwe (int):
        severity (int):
        is_executable (bool):
        cx_description_id (int):
        query_description_id (str):
   """
    id: int = None
    source: str = None
    level: str = None
    path: str = None
    modified: str = None
    cwe: int = None
    severity: int = None
    is_executable: bool = None
    cx_description_id: int = None
    query_description_id: str = None


def construct_query(item):
    return Query(
        id=item.get("id"),
        source=item.get("source"),
        level=item.get("level"),
        path=item.get("path"),
        modified=item.get("modified"),
        cwe=item.get("cwe"),
        severity=item.get("severity"),
        is_executable=item.get("isExecutable"),
        cx_description_id=item.get("cxDescriptionID"),
        query_description_id=item.get("queryDescriptionID")
    )
