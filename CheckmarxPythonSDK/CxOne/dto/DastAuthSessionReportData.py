from dataclasses import dataclass, field
from typing import List, Optional

from .DastAuthSessionLoginStep import DastAuthSessionLoginStep
from .DastAuthSessionStatisticItem import DastAuthSessionStatisticItem
from .DastAuthSessionSummaryItem import DastAuthSessionSummaryItem


@dataclass
class DastAuthSessionReportData:
    """Response from GET /authSession/{envId}/reportData.

    Attributes:
        date (Optional[str]): When the auth test ran (date-time).
        method (Optional[str]): Auth method tested.
        url (Optional[str]): The environment's URL.
        auth_success (Optional[bool]): Whether authentication succeeded.
        environment_name (Optional[str]): The environment's domain/name.
        environment_created (Optional[str]): When the environment was
            created (date-time).
        summary (List[DastAuthSessionSummaryItem]): Pass/fail checklist.
        failure_items (List[str]): Failure descriptions, if any.
        config (Optional[dict]): The auth configuration tested, left as a
            raw dict (AuthSessionConfig has nested AuthConfig/
            VerificationConfig schemas not yet confirmed against a live
            response).
        af_env (Optional[str]): Internal auth-flow environment identifier.
        statistics (List[DastAuthSessionStatisticItem]): Numeric stats
            about the test run.
        login_steps (List[DastAuthSessionLoginStep]): Step-by-step login
            trace, when available.
        domains (List[str]): Domains visited during the test.
    """
    date: Optional[str] = None
    method: Optional[str] = None
    url: Optional[str] = None
    auth_success: Optional[bool] = None
    environment_name: Optional[str] = None
    environment_created: Optional[str] = None
    summary: List[DastAuthSessionSummaryItem] = field(default_factory=list)
    failure_items: List[str] = field(default_factory=list)
    config: Optional[dict] = None
    af_env: Optional[str] = None
    statistics: List[DastAuthSessionStatisticItem] = field(default_factory=list)
    login_steps: List[DastAuthSessionLoginStep] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSessionReportData":
        return cls(
            date=item.get("date"),
            method=item.get("method"),
            url=item.get("url"),
            auth_success=item.get("authSuccess"),
            environment_name=item.get("environmentName"),
            environment_created=item.get("environmentCreated"),
            summary=[
                DastAuthSessionSummaryItem.from_dict(s)
                for s in (item.get("summary") or [])
            ],
            failure_items=list(item.get("failureItems") or []),
            config=item.get("config"),
            af_env=item.get("afEnv"),
            statistics=[
                DastAuthSessionStatisticItem.from_dict(s)
                for s in (item.get("statistics") or [])
            ],
            login_steps=[
                DastAuthSessionLoginStep.from_dict(s)
                for s in (item.get("loginSteps") or [])
            ],
            domains=list(item.get("domains") or []),
        )
