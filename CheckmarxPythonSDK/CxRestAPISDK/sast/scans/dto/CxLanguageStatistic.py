from dataclasses import dataclass
from typing import Optional


@dataclass
class CxLanguageStatistic:

    language: Optional[str] = None
    parsed_successfully_count: Optional[int] = None
    parsed_unsuccessfully_count: Optional[int] = None
    parsed_partially_count: Optional[int] = None
    successful_loc: Optional[int] = None
    unsuccessful_loc: Optional[int] = None
    scanned_successfully_loc_percentage: Optional[float] = None
    count_of_dom_objects: Optional[int] = None

    @classmethod
    def from_dict(cls, language: str, item: dict) -> "CxLanguageStatistic":
        return cls(
            language=language,
            parsed_successfully_count=item.get("parsedFiles", {}).get(
                "parsedSuccessfullyCount"
            ),
            parsed_unsuccessfully_count=item.get("parsedFiles", {}).get(
                "parsedUnsuccessfullyCount"
            ),
            parsed_partially_count=item.get("parsedFiles", {}).get(
                "parsedPartiallyCount"
            ),
            successful_loc=item.get("scannedLOCPerLanguage", {}).get("successfulLOC"),
            unsuccessful_loc=item.get("scannedLOCPerLanguage", {}).get(
                "unsuccessfulLOC"
            ),
            scanned_successfully_loc_percentage=item.get(
                "scannedLOCPerLanguage", {}
            ).get("scannedSuccessfullyLOCPercentage"),
            count_of_dom_objects=item.get("countOfDomObjects"),
        )
