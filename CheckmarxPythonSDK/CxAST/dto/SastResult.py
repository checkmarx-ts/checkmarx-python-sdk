from .ResultNode import ResultNode


class SastResult(object):
    def __init__(self, result_id, result_hash=None, query_id=None, query_name=None, language_name=None,
                 query_group=None, cwe_id=None, severity=None, similarity_id=None, confidence_level=None,
                 compliances=None, first_scan_id=None, first_found_at=None,
                 path_system_id_by_simi_and_files_paths=None, status=None, found_at=None, nodes=None,
                 state=None):
        """

        Args:
            result_id (str): ID of the result
            result_hash (str): ID of the path id system wide
            query_id (int): Query ID
            query_name (str): Query name
            language_name (str): Language name
            query_group (str): Query group name
            cwe_id (int): Query Common Weakness Enumeration ID
            severity (str): Severity enum of a result.
                            Enum:
                            [ HIGH, MEDIUM, LOW, INFO ]
            similarity_id (int): ID of the Similarity feature (Indicator to identify a result by its
                            first and last nodes)
            confidence_level (int): Confidence Level of the exsiting of the result
            compliances (str):
            first_scan_id (str): ID of the first scan id by resultHash
            first_found_at (str): date of the first found by resultHash
            path_system_id_by_simi_and_files_paths (str): ID created from queryMetaInfo + similarityID + files name.
            status (str): Status enum of a result
                        Enum:
                        [ NEW, RECURRENT, FIXED ]
            found_at (str): Creation date of the result
            nodes (list of ResultNode): array of the nodes. will be included only if the include-nodes parameter is true
            state:
        """
        self.ID = result_id
        self.resultHash = result_hash
        self.queryID = query_id
        self.queryName = query_name
        self.languageName = language_name
        self.group = query_group
        self.cweID = cwe_id
        self.severity = severity
        self.similarityID = similarity_id
        self.confidenceLevel = confidence_level
        self.compliances = compliances
        self.firstScanID = first_scan_id
        self.firstFoundAt = first_found_at
        self.pathSystemIDBySimiAndFilesPaths = path_system_id_by_simi_and_files_paths
        self.status = status
        self.foundAt = found_at
        self.nodes = nodes
        self.state = state

    def __str__(self):
        return """SastResult(ID={}, resultHash={}, queryID={}, queryName={}, languageName={}, group={}, 
        cweID={}, severity={}, similarityID={}, confidenceLevel={}, compliances={}, firstScanID={}, 
        firstFoundAt={}, pathSystemIDBySimiAndFilesPaths={}, status={}, foundAt={}, nodes={}, state={})""".format(
            self.ID,
            self.resultHash,
            self.queryID,
            self.queryName,
            self.languageName,
            self.group,
            self.cweID,
            self.severity,
            self.similarityID,
            self.confidenceLevel,
            self.compliances,
            self.firstScanID,
            self.firstFoundAt,
            self.pathSystemIDBySimiAndFilesPaths,
            self.status,
            self.foundAt,
            self.nodes,
            self.state,
        )
