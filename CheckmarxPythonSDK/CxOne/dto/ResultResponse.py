class ResultResponse(object):

    def __init__(self, vulnerability_id: str, source_file: str, source_line: int, source_id: int, source_name: str,
                 source_type: str, destination_file: str, destination_line: int, destination_id: int,
                 destination_name: str, destination_type: str, state: str, path_size: int):
        self.vulnerabilityId = vulnerability_id
        self.sourceFile = source_file
        self.sourceLine = source_line
        self.sourceId = source_id
        self.sourceName = source_name
        self.sourceType = source_type
        self.destinationFile = destination_file
        self.destinationLine = destination_line
        self.destinationId = destination_id
        self.destinationName = destination_name
        self.destinationType = destination_type
        self.state = state
        self.pathSize = path_size

    def __str__(self):
        return (f"ResultResponse(vulnerabilityId={self.vulnerabilityId}, sourceFile={self.sourceFile}, "
                f"sourceLine={self.sourceLine},"
                f"sourceId={self.sourceId}, sourceName={self.sourceName}, sourceType={self.sourceType}, "
                f"destinationFile={self.destinationFile}, destinationLine={self.destinationLine}, "
                f"destinationId={self.destinationId}, destinationName={self.destinationName},"
                f"destinationType={self.destinationType}, state={self.state}, pathSize={self.pathSize})")

    def to_dict(self):
        return {
            "vulnerabilityId": self.vulnerabilityId,
            "sourceFile": self.sourceFile,
            "sourceLine": self.sourceLine,
            "sourceId": self.sourceId,
            "sourceName": self.sourceName,
            "sourceType": self.sourceType,
            "destinationFile": self.destinationFile,
            "destinationLine": self.destinationLine,
            "destinationId": self.destinationId,
            "destinationName": self.destinationName,
            "destinationType": self.destinationType,
            "state": self.state,
            "pathSize": self.pathSize,
        }
