# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxDateAndTime:
    """
    scan date and time
    """

    started_on: Optional[str] = None
    finished_on: Optional[str] = None
    engine_started_on: Optional[str] = None
    engine_finished_on: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxDateAndTime":
        return cls(
            started_on=item.get("startedOn"),
            finished_on=item.get("finishedOn"),
            engine_started_on=item.get("engineStartedOn"),
            engine_finished_on=item.get("engineFinishedOn"),
        )
