class QuerySummary(object):
    def __init__(self, query_id, query_name, severity, count):
        """

        Args:
            query_id (str):
            query_name (str):
            severity (str): Severity enum of a result. Enum: [ HIGH, MEDIUM, LOW, INFO ]
            count (int):
        """
        self.queryID = query_id
        self.queryName = query_name
        self.severity = severity
        self.count = count

    def __str__(self):
        return """QuerySummary(queryID={}, queryName={}, severity={}, count={})""".format(
            self.queryID, self.queryName, self.severity, self.count
        )
