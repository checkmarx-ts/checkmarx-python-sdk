# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxProjectExcludeSettings:
    """
    project exclude settings
    """

    project_id: Optional[int] = None
    exclude_folders_pattern: Optional[str] = None
    exclude_files_pattern: Optional[str] = None
    link: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxProjectExcludeSettings":
        from .CxLink import CxLink

        return cls(
            project_id=item.get("projectId"),
            exclude_folders_pattern=item.get("excludeFoldersPattern"),
            exclude_files_pattern=item.get("excludeFilesPattern"),
            link=CxLink.from_dict(item.get("link") or {}),
        )
