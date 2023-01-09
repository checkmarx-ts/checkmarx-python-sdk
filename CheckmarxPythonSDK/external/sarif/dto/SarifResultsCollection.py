from .SarifRun import SarifRun


class SarifResultsCollection:
    def __init__(self, schema, version, runs):
        """

        Args:
            schema (str):
            version (str):
            runs (list of SarifRun):
        """
        self.Schema = schema
        self.Version = version
        self.Runs = runs

    def __str__(self):
        return f"SarifResultsCollection("\
               f"schema={self.Schema}, "\
               f"version={self.Version}, "\
               f"runs={self.Runs} "\
               f")"
