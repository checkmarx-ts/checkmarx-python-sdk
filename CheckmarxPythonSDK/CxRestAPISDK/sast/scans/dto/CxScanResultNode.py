from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanResultNode:

    id: Optional[int] = None
    order: Optional[int] = None
    short_name: Optional[str] = None
    full_name: Optional[str] = None
    file_name: Optional[str] = None
    folder: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    length: Optional[int] = None
    method_line: Optional[int] = None
    source_url: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanResultNode":
        return cls(
            id=item.get("id"),
            order=item.get("order"),
            short_name=item.get("shortName"),
            full_name=item.get("fullName"),
            file_name=item.get("fileName"),
            folder=item.get("folder"),
            line=item.get("line"),
            column=item.get("column"),
            length=item.get("length"),
            method_line=item.get("methodLine"),
            source_url=item.get("sourceUrl"),
        )
