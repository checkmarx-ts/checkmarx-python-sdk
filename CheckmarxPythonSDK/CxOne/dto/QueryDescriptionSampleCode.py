from dataclasses import dataclass


@dataclass
class QueryDescriptionSampleCode:
    """

    Args:
        programming_language (str):
        code (str):
        title (str):
    """
    programming_language: str
    code: str
    title: str


def construct_query_description_sample_code(item):
    return QueryDescriptionSampleCode(
        programming_language=item.get("progLanguage"),
        code=item.get("code"),
        title=item.get("title")
    )
