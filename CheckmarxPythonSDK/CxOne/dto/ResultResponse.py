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

    def to_dict(self):
        return {
            "vulnerabilityId": self.vulnerability_id,
            "sourceFile": self.source_file,
            "sourceLine": self.source_line,
            "sourceId": self.source_id,
            "sourceName": self.source_name,
            "sourceType": self.source_type,
            "destinationFile": self.destination_file,
            "destinationLine": self.destination_line,
            "destinationId": self.destination_id,
            "destinationName": self.destination_name,
            "destinationType": self.destination_type,
            "state": self.state,
            "pathSize": self.path_size,
        }


def construct_result_response(item):
    return ResultResponse(
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
        path_size=item.get("pathSize")
    )
