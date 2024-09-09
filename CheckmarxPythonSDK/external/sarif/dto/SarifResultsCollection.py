from .SarifRun import SarifRun


class SarifResultsCollection:
    def __init__(self, schema, version, runs):
        """

        Args:
            schema (str):
            version (str):
            runs (list of SarifRun):
        """
        self.schema = schema
        self.version = version
        self.runs = runs

    def __str__(self):
        return f"SarifResultsCollection("\
               f"schema={self.schema}, "\
               f"version={self.version}, "\
               f"runs={self.runs} "\
               f")"
