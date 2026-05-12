from dataclasses import dataclass


@dataclass
class DebugMessage:
    message_line: int = None
    debug_message: str = None
    timestamp: str = None
