from dataclasses import dataclass


@dataclass
class Metadata:
    cwe: int
    severity: int
    is_executable: bool
    cx_description_id: int


def construct_metadata(item):
    return Metadata(
        cwe=item.get("Cwe"),
        severity=item.get("Severity"),
        is_executable=item.get("IsExecutable"),
        cx_description_id=item.get("CxDescriptionID")
    )
