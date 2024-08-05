class QueryDetails(object):

    def __init__(self, query_id, cwe_id, language, group, query_name, severity, query_description_id, custom):
        """

        Args:
            query_id (str):
            cwe_id (int):
            language (str):
            group (str):
            query_name (str):
            severity (str):
            query_description_id (int):
            custom (bool):
        """
        self.query_id = query_id
        self.cwe_id = cwe_id
        self.language = language
        self.group = group
        self.query_name = query_name
        self.severity = severity
        self.query_description_id = query_description_id
        self.custom = custom

    def __str__(self):
        return f"""QueryDetails(
        query_id={self.query_id},
        cwe_id={self.cwe_id},
        language={self.language},
        group={self.group},
        query_name={self.query_name},
        severity={self.severity},
        query_description_id={self.query_description_id},
        custom={self.custom},
        )"""
