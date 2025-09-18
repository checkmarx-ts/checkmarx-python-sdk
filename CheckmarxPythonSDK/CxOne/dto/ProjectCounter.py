from dataclasses import dataclass


@dataclass
class ProjectCounter:
    """

      Attributes:
          value (str):
          count (int):
      """
    value: str = None
    count: int = None


def construct_project_counter(item):
    return ProjectCounter(
        value=item.get("value"),
        count=item.get("count")
    )
