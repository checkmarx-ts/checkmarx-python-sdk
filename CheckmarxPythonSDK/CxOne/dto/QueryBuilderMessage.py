from dataclasses import dataclass


@dataclass
class QueryBuilderMessage:
    role: str = None
    content: str = None


def construct_query_builder_message(item):
    return QueryBuilderMessage(
        role=item.get("role"),
        content=item.get("content")
    )
