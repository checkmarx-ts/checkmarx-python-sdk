from dataclasses import dataclass
from typing import List


@dataclass
class ScheduleInput:
    name: str = None
    start_time: str = None
    frequency: str = None
    days: List[str] = None
    engines: List[str] = None
    branch: str = None
    tags: dict = None
    active: bool = None
    new_project_id: str = None
