from dataclasses import dataclass
from typing import List, Union
from .DastResultNote import DastResultNote
from .DastResultChangelogEntry import DastResultChangelogEntry
from .DastResultStatus import DastResultStatus
from .DastResultState import DastResultState


@dataclass
class DastResultDetail:
    """Detailed info about a single result from
    GET /api/dast/mfe-results/results/info/{result_id}/{scan_id}.

    Superset of DastResult fields plus diagnostic context
    (request/response bodies and headers, attack/evidence, score,
    structured notes/changelog).
    """
    id: str = None
    severity: str = None
    confidence: str = None
    state: Union[DastResultState, str] = None
    name: str = None
    description: str = None
    url: str = None
    method: str = None
    path: str = None
    created_at: str = None
    attack: str = None
    evidence: str = None
    solution: str = None
    score: float = None
    request_header: str = None
    request_body: str = None
    response_header: str = None
    response_body: str = None
    updated_at: str = None
    comment: str = None
    ref: List[str] = None
    owasp: List[str] = None
    status: Union[DastResultStatus, str] = None
    environment_id: str = None
    alert_status: str = None
    params: str = None
    other_info: str = None
    notes_data: List[DastResultNote] = None
    changelog_data: List[DastResultChangelogEntry] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastResultDetail":
        return cls(
            id=item.get("id"),
            severity=item.get("severity"),
            confidence=item.get("confidence"),
            state=item.get("state"),
            name=item.get("name"),
            description=item.get("description"),
            url=item.get("url"),
            method=item.get("method"),
            path=item.get("path"),
            created_at=item.get("created_at"),
            attack=item.get("attack"),
            evidence=item.get("evidence"),
            solution=item.get("solution"),
            score=item.get("score"),
            request_header=item.get("request_header"),
            request_body=item.get("request_body"),
            response_header=item.get("response_header"),
            response_body=item.get("response_body"),
            updated_at=item.get("updated_at"),
            comment=item.get("comment"),
            ref=item.get("ref"),
            owasp=item.get("owasp"),
            status=item.get("status"),
            environment_id=item.get("environment_id"),
            alert_status=item.get("alert_status"),
            params=item.get("params"),
            other_info=item.get("other_info"),
            notes_data=[
                DastResultNote.from_dict(n) for n in (item.get("notes_data") or [])
            ],
            changelog_data=[
                DastResultChangelogEntry.from_dict(c) for c in (item.get("changelog_data") or [])
            ],
        )
