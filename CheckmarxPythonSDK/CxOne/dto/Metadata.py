from dataclasses import dataclass


@dataclass
class Metadata:
    Cwe: int = None
    Severity: int = None
    IsExecutable: bool = None
    CxDescriptionID: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "Metadata":
        return cls(
            Cwe=item.get("Cwe"),
            Severity=item.get("Severity"),
            IsExecutable=item.get("IsExecutable"),
            CxDescriptionID=item.get("CxDescriptionID"),
        )
