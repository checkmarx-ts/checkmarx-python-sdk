from dataclasses import dataclass, field
from typing import List, Optional

from .RemediationAnalysis import RemediationAnalysis
from .FileChange import FileChange
from .TestCreation import TestCreation


@dataclass
class RemediationData:
    """Generated remediation analysis, code changes, and test information."""

    error: Optional[str] = None
    summary: str = None
    analysis: Optional[RemediationAnalysis] = None
    pr_title: str = None
    file_changes: List[FileChange] = field(default_factory=list)
    test_creation: Optional[TestCreation] = None

    @classmethod
    def from_dict(cls, item: dict) -> "RemediationData":
        return cls(
            error=item.get("error"),
            summary=item.get("summary"),
            analysis=(
                RemediationAnalysis.from_dict(item["analysis"])
                if item.get("analysis")
                else None
            ),
            pr_title=item.get("pr_title"),
            file_changes=[FileChange.from_dict(f) for f in item.get("file_changes", [])],
            test_creation=(
                TestCreation.from_dict(item["test_creation"])
                if item.get("test_creation")
                else None
            ),
        )
