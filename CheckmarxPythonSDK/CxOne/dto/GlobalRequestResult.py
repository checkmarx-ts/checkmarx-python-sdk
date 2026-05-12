from dataclasses import dataclass


@dataclass
class GlobalRequestResult:
    failed_requests: ... = None
    success_requests: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "GlobalRequestResult":
        return cls(
            failed_requests=item.get("failedRequests"),
            success_requests=item.get("successRequests"),
        )
