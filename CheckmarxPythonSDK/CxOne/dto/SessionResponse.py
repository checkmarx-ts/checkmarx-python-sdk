from dataclasses import dataclass


@dataclass
class SessionResponse:
    id: str = None
    status: str = None
    scan_id: str = None


def construct_session_response(item):
    return SessionResponse(
        id=item.get("id"),
        status=item.get("status"),
        scan_id=item.get("scanId")
    )
