from dataclasses import dataclass
from .DastLastRiskRating import DastLastRiskRating
from .DastAuthSuccess import DastAuthSuccess
from .DastTunnelState import DastTunnelState


@dataclass
class DastEnvironmentFilter:
    """Shape for the `filter` and `match` query parameters of
    GET /api/dast/scans/environments.

    `filter` does partial-match; `match` does exact-match — same fields.
    Pass an instance to DastScanAPI.get_environments(filter=...) or match=...
    """
    domain: str = None
    url: str = None
    scan_type: str = None
    environment_id: str = None
    project_id: str = None
    last_risk_rating: DastLastRiskRating = None
    auth_success: DastAuthSuccess = None
    tunnel_state: DastTunnelState = None

    def to_dict(self) -> dict:
        """Serialize to the JSON-object shape the API expects, using its
        camelCase keys and dropping unset fields."""
        raw = {
            "domain": self.domain,
            "url": self.url,
            "scantype": self.scan_type,
            "environmentId": self.environment_id,
            "projectId": self.project_id,
            "lastRiskRating": (
                self.last_risk_rating.value
                if isinstance(self.last_risk_rating, DastLastRiskRating)
                else self.last_risk_rating
            ),
            "authSuccess": (
                self.auth_success.value
                if isinstance(self.auth_success, DastAuthSuccess)
                else self.auth_success
            ),
            "tunnelState": (
                self.tunnel_state.value
                if isinstance(self.tunnel_state, DastTunnelState)
                else self.tunnel_state
            ),
        }
        return {k: v for k, v in raw.items() if v is not None}
