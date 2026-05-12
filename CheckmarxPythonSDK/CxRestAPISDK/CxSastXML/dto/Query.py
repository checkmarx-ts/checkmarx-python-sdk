from dataclasses import dataclass
from typing import List, Optional

from .Result import Result


@dataclass
class Query:
    query_id: Optional[int] = None
    categories: Optional[str] = None
    cwe_id: Optional[int] = None
    query_name: Optional[str] = None
    query_group: Optional[str] = None
    severity: Optional[str] = None
    language: Optional[str] = None
    language_hash: Optional[str] = None
    language_change_date: Optional[str] = None
    severity_index: Optional[int] = None
    query_path: Optional[str] = None
    query_version_code: Optional[int] = None
    results: Optional[List[Result]] = None

    @classmethod
    def from_dict(cls, item: dict, results=None) -> "Query":
        return cls(
            query_id=int(item.get("id")),
            categories=item.get("categories"),
            cwe_id=int(item.get("cweId")),
            query_name=item.get("name"),
            query_group=item.get("group"),
            severity=item.get("Severity"),
            language=item.get("Language"),
            language_hash=item.get("LanguageHash"),
            language_change_date=item.get("LanguageChangeDate"),
            severity_index=int(item.get("SeverityIndex")),
            query_path=item.get("QueryPath"),
            query_version_code=int(item.get("QueryVersionCode")),
            results=results,
        )
