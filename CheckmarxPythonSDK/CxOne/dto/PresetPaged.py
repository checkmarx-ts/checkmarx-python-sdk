from dataclasses import dataclass
from .PresetSummary import PresetSummary, construct_preset_summary
from typing import List


@dataclass
class PresetPaged:
    """

    Args:
        total_count (int):
        presets (list of PresetSummary):
    """
    total_count: int
    presets: List[PresetSummary]


def construct_preset_paged(item):
    return PresetPaged(
        total_count=item.get("totalCount"),
        presets=[
            construct_preset_summary(preset) for preset in item.get("presets", [])
        ]
    )
