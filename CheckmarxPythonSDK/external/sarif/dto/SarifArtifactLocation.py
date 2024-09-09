class SarifArtifactLocation:
    def __init__(self, uri):
        """

        Args:
            uri (str):
        """
        self.uri = uri

    def __str__(self):
        return f"SarifArtifactLocation(" \
               f"uri={self.uri}"\
               f")"
