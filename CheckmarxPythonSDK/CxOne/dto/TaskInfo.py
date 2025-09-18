from dataclasses import dataclass


@dataclass
class TaskInfo:
    """

    Args:
        source (str): The service that generated the task event.
        timestamp (str): The time of the task event.
        info: An informative message describing the task event.
    """
    source: str
    timestamp: str
    info: str


def construct_task_info(item):
    return TaskInfo(
        source=item.get("source"),
        timestamp=item.get("timestamp"),
        info=item.get("info")
    )
