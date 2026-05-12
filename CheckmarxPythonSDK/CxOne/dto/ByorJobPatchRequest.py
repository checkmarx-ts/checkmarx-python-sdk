from dataclasses import dataclass


@dataclass
class ByorJobPatchRequest:
    status: str = None  # Canceled is the only valid input.
