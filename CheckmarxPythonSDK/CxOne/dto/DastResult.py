from dataclasses import dataclass
from typing import List, Union
from .DastResultStatus import DastResultStatus
from .DastResultState import DastResultState
from .DastScanType import DastScanType


@dataclass
class DastResult:
    """One result/risk row from GET /api/dast/mfe-results/results/{scan_id}.

    Wire keys are snake_case throughout (doc shows cweId/environmentId
    camelCase, but live response uses cwe_id/environment_id). cwe_id
    is returned as a string (e.g. "-1"), not int.

    notes_data and changelog_data are documented as array[object] with
    no sub-schema; left as raw List[dict] until shapes are pinned down.
    The doc's `chagelog_data` typo is fixed in the live API.

    similarity_id_2 is documented as INTERNAL USE and not surfaced in
    the public response — omitted from this DTO.
    """
    id: str = None
    severity: str = None
    state: Union[DastResultState, str] = None
    name: str = None
    description: str = None
    url: str = None
    method: str = None
    path: str = None
    cwe_id: str = None
    environment_id: str = None
    notes_data: List[dict] = None
    owasp: List[str] = None
    solution: str = None
    status: Union[DastResultStatus, str] = None
    scan_type: Union[DastScanType, str] = None
    changelog_data: List[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResult":
        return cls(
            id=item.get("id"),
            severity=item.get("severity"),
            state=item.get("state"),
            name=item.get("name"),
            description=item.get("description"),
            url=item.get("url"),
            method=item.get("method"),
            path=item.get("path"),
            cwe_id=item.get("cwe_id"),
            environment_id=item.get("environment_id"),
            notes_data=item.get("notes_data"),
            owasp=item.get("owasp"),
            solution=item.get("solution"),
            status=item.get("status"),
            scan_type=item.get("scan_type"),
            changelog_data=item.get("changelog_data"),
        )
