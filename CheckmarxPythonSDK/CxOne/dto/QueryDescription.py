from dataclasses import dataclass
from typing import List
from .QueryDescriptionSampleCode import QueryDescriptionSampleCode


@dataclass
class QueryDescription:
    query_id: str = None
    query_name: str = None
    result_description: str = None
    risk: str = None
    cause: str = None
    general_recommendations: str = None
    sample: List[QueryDescriptionSampleCode] = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueryDescription":
        return cls(
            query_id=item.get("queryId"),
            query_name=item.get("queryName"),
            result_description=item.get("resultDescription"),
            risk=item.get("risk"),
            cause=item.get("cause"),
            general_recommendations=item.get("generalRecommendations"),
            sample=[
                QueryDescriptionSampleCode.from_dict(s)
                for s in (item.get("sample") or [])
            ],
        )
