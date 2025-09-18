from dataclasses import dataclass


@dataclass
class DebugMessage:
    message_line: int = None
    debug_message: str = None
    timestamp: str = None


def construct_debug_message(item):
    return DebugMessage(
        message_line=item.get("messageLine"),
        debug_message=item.get("debugMessage"),
        timestamp=item.get("timestamp")
    )
