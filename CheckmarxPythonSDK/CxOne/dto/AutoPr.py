from dataclasses import dataclass
from typing import Optional


@dataclass
class AutoPr:
    """Information about the automatic pull request operation."""

    status: str = None
    url: Optional[str] = None
    error_msg: str = None
    file_url: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "AutoPr":
        return cls(
            status=item.get("status"),
            url=item.get("url"),
            error_msg=item.get("error_msg"),
            file_url=item.get("file_url"),
        )
