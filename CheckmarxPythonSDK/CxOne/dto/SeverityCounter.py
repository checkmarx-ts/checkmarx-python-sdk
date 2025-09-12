from dataclasses import dataclass


@dataclass
class SeverityCounter:
    severity: str = None  # The severity level of the vulnerability.
    counter: int = None  # The number of vulnerabilities found at this severity level.


def construct_severity_counter(item):
    return SeverityCounter(
        severity=item.get("severity"),
        counter=item.get("counter"),
    )
