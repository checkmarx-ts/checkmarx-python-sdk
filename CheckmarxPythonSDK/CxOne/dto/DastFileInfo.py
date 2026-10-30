from dataclasses import dataclass
from typing import Optional


@dataclass
class DastFileInfo:
    """A `{FileName, Size, Content}` file object, as returned embedded in
    an auth session (File/APIFile fields) or a proxy recorder file.

    `content` is base64-encoded (format: byte) file content.
    """
    file_name: Optional[str] = None
    size: Optional[int] = None
    content: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastFileInfo":
        return cls(
            file_name=item.get("FileName"),
            size=item.get("Size"),
            content=item.get("Content"),
        )
