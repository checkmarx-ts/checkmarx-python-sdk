from dataclasses import dataclass


@dataclass
class SastStatus:
    ready: bool = None
    message: str = None


def construct_sast_status(item):
    return SastStatus(
        ready=item.get("ready"),
        message=item.get("message")
    )
