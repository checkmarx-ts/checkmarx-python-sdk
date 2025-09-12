from dataclasses import dataclass


@dataclass
class Error:
    message: str = None
    type: str = None
    code: int = None
