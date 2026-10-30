from dataclasses import dataclass, field
from typing import List, Optional

from .DastSequenceScriptsChain import DastSequenceScriptsChain


@dataclass
class DastSequenceScriptsResponse:
    """Response from GET /environments/{envId}/sequence-scripts.

    Attributes:
        chains (List[DastSequenceScriptsChain]): The environment's
            sequences, as ordered recording-filename chains, for CLI use.
        archive (Optional[str]): Base64-encoded zip archive containing
            the recording files for all chains.
    """
    chains: List[DastSequenceScriptsChain] = field(default_factory=list)
    archive: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastSequenceScriptsResponse":
        return cls(
            chains=[
                DastSequenceScriptsChain.from_dict(c) for c in (item.get("chains") or [])
            ],
            archive=item.get("archive"),
        )
