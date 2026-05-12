from dataclasses import dataclass


@dataclass
class QueryDescriptionSampleCode:
    programming_language: str = None
    code: str = None
    title: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueryDescriptionSampleCode":
        return cls(
            programming_language=item.get("progLanguage"),
            code=item.get("code"),
            title=item.get("title"),
        )
