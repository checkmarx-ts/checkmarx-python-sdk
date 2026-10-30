from dataclasses import dataclass, field
from typing import List


@dataclass
class DastSequenceScriptsChain:
    """An entry in `chains[]` on GET /environments/{envId}/sequence-scripts.

    Attributes:
        recordings (List[str]): Recording filenames (e.g. "myRecording.zst")
            making up this chain, in order.
    """
    recordings: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequenceScriptsChain":
        return cls(recordings=list(item.get("recordings") or []))
