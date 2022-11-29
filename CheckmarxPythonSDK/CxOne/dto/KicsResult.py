class KicsResult(object):
    def __init__(self, kics_result_id, similarity_id, severity, first_scan_id, first_found_at, found_at, status, state,
                 kics_type, query_id, query_name, query_group, query_url, file_name, line, platform, issue_type,
                 search_key, search_value, expected_value, actual_value, value, description, comments, category):
        """

        Args:
            kics_result_id (str): ID of the result
            similarity_id (int): ID of the Similarity feature (Indicator to identify a result by its first and last
                    nodes)
            severity (str): Severity enum of a result.
            first_scan_id (str): ID of the first scan id by resultHash
            first_found_at (str): date of the first found by resultHash
            found_at (str): Creation date of the result
            status (str): Status enum of a result
                        Enum:
                        [ NEW, RECURRENT, FIXED ]
            state (str): state enum of a result.
                        Enum:
                        [ TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT ]
            kics_type (str):
            query_id (int): Query ID
            query_name (str): Query name
            query_group (str): Query group name
            query_url (str):
            file_name (str):
            line (int):
            platform (str):
            issue_type (str):
            search_key (str):
            search_value (int):
            expected_value (str):
            actual_value (str):
            value (str):
            description (str):
            comments (str):
            category (str):
        """
        self.ID = kics_result_id
        self.similarityID = similarity_id
        self.severity = severity
        self.firstScanID = first_scan_id
        self.firstFoundAt = first_found_at
        self.foundAt = found_at
        self.status = status
        self.state = state
        self.type = kics_type
        self.queryID = query_id
        self.queryName = query_name
        self.group = query_group
        self.queryUrl = query_url
        self.fileName = file_name
        self.line = line
        self.platform = platform
        self.issueType = issue_type
        self.searchKey = search_key
        self.searchValue = search_value
        self.expectedValue = expected_value
        self.actualValue = actual_value
        self.value = value
        self.description = description
        self.comments = comments
        self.category = category

    def __str__(self):
        return """KicsResult(ID={}, similarityID={}, severity={}, firstScanID={}, firstFoundAt={}, foundAt={}, 
        status={}, state={}, type={}, queryID={}, queryName={}, group={}, queryUrl={}, fileName={}, line={}, 
        platform={}, issueType={}, searchKey={}, searchValue={}, expectedValue={}, actualValue={},
        value={}, description={}, comments={}, category={})""".format(
            self.ID,
            self.similarityID,
            self.severity,
            self.firstScanID,
            self.firstFoundAt,
            self.foundAt,
            self.status,
            self.state,
            self.type,
            self.queryID,
            self.queryName,
            self.group,
            self.queryUrl,
            self.fileName,
            self.line,
            self.platform,
            self.issueType,
            self.searchKey,
            self.searchValue,
            self.expectedValue,
            self.actualValue,
            self.value,
            self.description,
            self.comments,
            self.category,
        )
