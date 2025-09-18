from dataclasses import dataclass
from typing import List
from .QueryDescriptionSampleCode import QueryDescriptionSampleCode, construct_query_description_sample_code


@dataclass
class QueryDescription:
    """

    Args:
        query_id (str):
        query_name (str):
        result_description (str):
        risk (str):
        cause (str):
        general_recommendations (str):
        sample (list of QueryDescriptionSampleCode):
    """
    query_id: str
    query_name: str
    result_description: str
    risk: str
    cause: str
    general_recommendations: str
    sample: List[QueryDescriptionSampleCode]


def construct_query_description(item):
    return QueryDescription(
        query_id=item.get("queryId"),
        query_name=item.get("queryName"),
        result_description=item.get("resultDescription"),
        risk=item.get("risk"),
        cause=item.get("cause"),
        general_recommendations=item.get("generalRecommendations"),
        sample=[
            construct_query_description_sample_code(sample_code) for sample_code in item.get("sample", [])
        ]
    )
