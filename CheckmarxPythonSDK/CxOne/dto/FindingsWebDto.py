from dataclasses import dataclass
from typing import Optional


@dataclass
class FindingsWebDto:
    """A SAST/IaC finding as referenced from a policy violation.

    Attributes:
        resultId (Optional[str]): The result ID.
        similarityId (Optional[str]): The similarity ID.
        queryId (Optional[str]): The query ID that produced the finding.
        queryName (Optional[str]): The query name.
        severity (Optional[str]): Severity. Values: CRITICAL, HIGH, MEDIUM, LOW, INFO.
        cweId (Optional[int]): CWE ID, if applicable.
        fileName (Optional[str]): File the finding was detected in.
        line (Optional[int]): Line number of the finding.
        description (Optional[str]): Finding description.
        stateName (Optional[str]): Current result state.
    """

    resultId: Optional[str] = None
    similarityId: Optional[str] = None
    queryId: Optional[str] = None
    queryName: Optional[str] = None
    severity: Optional[str] = None
    cweId: Optional[int] = None
    fileName: Optional[str] = None
    line: Optional[int] = None
    description: Optional[str] = None
    stateName: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "FindingsWebDto":
        return cls(
            resultId=item.get("resultId"),
            similarityId=item.get("similarityId"),
            queryId=item.get("queryId"),
            queryName=item.get("queryName"),
            severity=item.get("severity"),
            cweId=item.get("cweId"),
            fileName=item.get("fileName"),
            line=item.get("line"),
            description=item.get("description"),
            stateName=item.get("stateName"),
        )
