class Query(object):
    def __init__(self, source, level, path, modified, cwe, severity, is_executable, cx_description_id,
                 query_description_id):
        """

        Args:
            source (str):
            level (str):
            path (str):
            modified (str):
            cwe (int):
            severity (int):
            is_executable (bool):
            cx_description_id (int):
            query_description_id (str):
        """
        self.source = source
        self.level = level
        self.path = path
        self.modified = modified
        self.Cwe = cwe
        self.Severity = severity
        self.IsExecutable = is_executable
        self.CxDescriptionID = cx_description_id
        self.QueryDescriptionID = query_description_id

    def __str__(self):
        return """Query(source={}, level={}, modified={}, Cwe={}, Severity={}, IsExecutable={}, CxDescriptionID={}, 
        QueryDescriptionID={})""".format(
            self.source, self.level, self.modified, self.Cwe, self.Severity, self.IsExecutable, self.CxDescriptionID,
            self.QueryDescriptionID
        )
