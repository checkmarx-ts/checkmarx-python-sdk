from dataclasses import dataclass, field
from typing import List, Optional

from .TestFile import TestFile


@dataclass
class TestCreation:
    """Information about tests generated for the remediation."""

    error: Optional[str] = None
    summary: str = None
    analysis: str = None
    test_files: List[TestFile] = field(default_factory=list)
    total_tests_created: int = 0
    coverage_areas: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "TestCreation":
        return cls(
            error=item.get("error"),
            summary=item.get("summary"),
            analysis=item.get("analysis"),
            test_files=[TestFile.from_dict(f) for f in item.get("test_files", [])],
            total_tests_created=item.get("total_tests_created", 0),
            coverage_areas=item.get("coverage_areas", []),
        )
