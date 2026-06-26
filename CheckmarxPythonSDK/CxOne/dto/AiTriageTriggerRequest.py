from dataclasses import dataclass, field
from typing import List

from .AiTriageVulnerability import AiTriageVulnerability


@dataclass
class AiTriageTriggerRequest:
    """Request body for POST /api/v1/ai-triage/trigger.

    Attributes:
        vulnerabilities (List[AiTriageVulnerability]): One or more
            vulnerabilities to triage. Currently supported for SAST and SCA
            scanners only.
    """

    vulnerabilities: List[AiTriageVulnerability] = field(default_factory=list)
