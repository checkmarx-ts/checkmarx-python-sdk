from dataclasses import dataclass
from typing import Optional


@dataclass
class DastTechnology:
    """An entry in the response of GET /technologies -- the canonical
    list of technology ids/categories EnvSettings.Technologies accepts.

    Attributes:
        tag (str): The technology's identifier.
        category (str): DB, Framework, Language, OS, Protocol, or WS.
    """
    tag: Optional[str] = None
    category: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastTechnology":
        return cls(tag=item.get("tag"), category=item.get("category"))
