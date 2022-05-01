class Result(object):
    def __init__(self, result_type, result_id, similarity_id, status, state, severity, confidence_level, created,
                 first_found_at, found_at, update_at, first_scan_id, description, data, comments,
                 vulnerability_details):
        """

        Args:
            result_type (str): Type of result indicates its engine.
            result_id (str): ID of the result.
            similarity_id (int): ID of the similarity feature indicates the identification of a result by its first and
                            last nodes.
            status (str): Status enum of a result
            state (str): State enum of a result.
            severity (str): Severity enum of a result.
            confidence_level (int): Confidence level of the exsitence of the result from 0 unknown to 5 high.
            created (str): Creation date of the result.
            first_found_at (str): Date of the first time the result was found.
            found_at (str): Date of finding the result.
            update_at (str): Date of last update of the result.
            first_scan_id (str): ID of the first scan id by resultHash
            description (str): Result query description
            data:
            comments:
            vulnerability_details:
        """
        self.type = result_type
        self.id = result_id
        self.similarityID = similarity_id
        self.status = status
        self.state = state
        self.severity = severity
        self.confidenceLevel = confidence_level
        self.created = created
        self.firstFoundAt = first_found_at
        self.foundAt = found_at
        self.updateAt = update_at
        self.firstScanID = first_scan_id
        self.description = description
        self.data = data
        self.comments = comments
        self.vulnerabilityDetails = vulnerability_details

    def __str__(self):
        return """Result(type={}, id={}, similarityID={}, status={}, state={}, severity={}, confidenceLevel={},
        created={}, firstFoundAt={}, foundAt={}, updateAt={}, firstScanID={}, description={}, data={}, comments={}, 
        vulnerabilityDetails={})""".format(
            self.type, self.id, self.similarityID, self.status, self.state, self.severity, self.confidenceLevel,
            self.created, self.firstFoundAt, self.foundAt, self.updateAt, self.firstScanID, self.description,
            self.data, self.comments, self.vulnerabilityDetails
        )
