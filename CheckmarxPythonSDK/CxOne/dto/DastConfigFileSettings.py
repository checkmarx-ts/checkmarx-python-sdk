from dataclasses import dataclass
from typing import List


@dataclass
class DastConfigFileSettings:
    """settings.configFileSettings on POST /api/dast/scans/environment."""
    exclude_paths: List[str] = None

    def to_dict(self) -> dict:
        raw = {"excludePaths": self.exclude_paths}
        return {k: v for k, v in raw.items() if v is not None}
