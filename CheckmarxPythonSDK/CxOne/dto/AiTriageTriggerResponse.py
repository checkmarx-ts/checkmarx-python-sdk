from dataclasses import dataclass


@dataclass
class AiTriageTriggerResponse:
    """Response from POST /api/v1/ai-triage/trigger.

    Attributes:
        processId (str): Unique identifier of the triggered AI Triage or AI
            Remediation process.
        status (str): Status of the triggered process. Allowed values:
            'in_progress', 'rejected'.
    """

    processId: str = None
    status: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "AiTriageTriggerResponse":
        return cls(
            processId=item.get("processId"),
            status=item.get("status"),
        )
