from dataclasses import dataclass
from .SeverityCounter import SeverityCounter, construct_severity_counter
from typing import List


@dataclass
class TotalCounters:
    severity_counters: List[SeverityCounter]


def construct_total_counters(item):
    return TotalCounters(
        severity_counters=[
           construct_severity_counter(severity_counter) for severity_counter in item.get("severityCounters", [])
        ]
    )
