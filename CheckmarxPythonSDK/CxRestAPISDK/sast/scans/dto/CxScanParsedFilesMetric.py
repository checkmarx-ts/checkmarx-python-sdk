from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanParsedFilesMetric:

    language: Optional[str] = None
    parsed_successfully: Optional[int] = None
    parsed_unsuccessfully: Optional[int] = None
    parsed_partially: Optional[int] = None

    @classmethod
    def from_dict(cls, language: str, item: dict) -> "CxScanParsedFilesMetric":
        return cls(
            language=language,
            parsed_successfully=item.get("parsedSuccessfully"),
            parsed_unsuccessfully=item.get("parsedUnsuccessfully"),
            parsed_partially=item.get("parsedPartially"),
        )
