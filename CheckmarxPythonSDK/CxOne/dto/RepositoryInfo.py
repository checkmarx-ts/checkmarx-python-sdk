from dataclasses import dataclass, field
from typing import List


@dataclass
class RepositoryInfo:
    path: str = ""
    excluded_subdirectories: List[str] = field(default_factory=list)
    description: str = ""
    programming_languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    dependency_management_systems: List[str] = field(default_factory=list)
    dependency_files: List[str] = field(default_factory=list)
    build_process_info: str = None
    build_system: str = None
    documentation: List[str] = field(default_factory=list)
    key_directories: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "RepositoryInfo":
        return cls(
            path=item.get("path", ""),
            excluded_subdirectories=item.get("excluded_subdirectories", []),
            description=item.get("description", ""),
            programming_languages=item.get("programming_languages", []),
            frameworks=item.get("frameworks", []),
            dependency_management_systems=item.get("dependency_management_systems", []),
            dependency_files=item.get("dependency_files", []),
            build_process_info=item.get("build_process_info"),
            build_system=item.get("build_system"),
            documentation=item.get("documentation", []),
            key_directories=item.get("key_directories", []),
        )
