from dataclasses import dataclass
from .DastScanAuthParameters import DastScanAuthParameters
from .DastScanAuthVerification import DastScanAuthVerification


@dataclass
class DastScanAuth:
    method: str = None
    parameters: DastScanAuthParameters = None
    verification: DastScanAuthVerification = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanAuth":
        return cls(
            method=item.get("Method"),
            parameters=DastScanAuthParameters.from_dict(item["Parameters"]) if item.get("Parameters") else None,
            verification=DastScanAuthVerification.from_dict(item["Verification"]) if item.get("Verification") else None,
        )
