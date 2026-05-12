from dataclasses import dataclass, field
from typing import List
from .PresetSummary import PresetSummary


@dataclass
class PresetPaged:
    total_count: int = None
    presets: List[PresetSummary] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "PresetPaged":
        return cls(
            total_count=item.get("totalCount"),
            presets=[PresetSummary.from_dict(p) for p in (item.get("presets") or [])],
        )
