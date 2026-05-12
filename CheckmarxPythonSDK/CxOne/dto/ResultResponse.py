from dataclasses import dataclass


@dataclass
class ResultResponse:
    vulnerability_id: str
    source_file: str
    source_line: int
    source_id: int
    source_name: str
    source_type: str
    destination_file: str
    destination_line: int
    destination_id: int
    destination_name: str
    destination_type: str
    state: str
    path_size: int

    @classmethod
    def from_dict(cls, item: dict) -> "ResultResponse":
        return cls(
            vulnerability_id=item.get("vulnerabilityId"),
            source_file=item.get("sourceFile"),
            source_line=item.get("sourceLine"),
            source_id=item.get("sourceId"),
            source_name=item.get("sourceName"),
            source_type=item.get("sourceType"),
            destination_file=item.get("destinationFile"),
            destination_line=item.get("destinationLine"),
            destination_id=item.get("destinationId"),
            destination_name=item.get("destinationName"),
            destination_type=item.get("destinationType"),
            state=item.get("state"),
            path_size=item.get("pathSize"),
        )
