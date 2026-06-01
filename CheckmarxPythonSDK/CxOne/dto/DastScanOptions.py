from dataclasses import dataclass
from typing import Union
from .DastScanOption import DastScanOption


@dataclass
class DastScanOptions:
    """settings.scanOptions on POST /api/dast/scans/environment."""
    scan_option: Union[DastScanOption, str] = None
    include_server: bool = None
    slow_app: bool = None

    def to_dict(self) -> dict:
        raw = {
            "scanOption": (
                self.scan_option.value if isinstance(self.scan_option, DastScanOption)
                else self.scan_option
            ),
            "includeServer": self.include_server,
            "slowApp": self.slow_app,
        }
        return {k: v for k, v in raw.items() if v is not None}
