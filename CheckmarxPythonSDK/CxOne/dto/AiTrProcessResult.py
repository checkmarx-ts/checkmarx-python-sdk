from dataclasses import dataclass

from .AiTriageVulnerability import AiTriageVulnerability


@dataclass
class AiTrProcessResult:
    """A single vulnerability result within a process status response.

    Attributes:
        projectId (str): Unique identifier of the project associated with the
            triggered process.
        identifier (AiTriageVulnerability): The vulnerability identifier that
            was submitted for the process.
        status (str): Current status of the process for this vulnerability.
            Allowed values: 'completed', 'failed'.
        error (str or None): Error details if the process failed; otherwise
            None.
    """

    projectId: str = None
    identifier: AiTriageVulnerability = None
    status: str = None
    error: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiTrProcessResult":
        identifier = None
        if item.get("identifier"):
            identifier = AiTriageVulnerability(
                projectId=item["identifier"].get("projectId"),
                similarityId=item["identifier"].get("similarityId"),
                attackVectorId=item["identifier"].get("attackVectorId"),
            )
        return cls(
            projectId=item.get("projectId"),
            identifier=identifier,
            status=item.get("status"),
            error=item.get("error"),
        )
