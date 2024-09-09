from .SarifArtifactLocation import SarifArtifactLocation
from .SarifRegion import SarifRegion
from .SarifPhysicalLocationPropertyBag import SarifPhysicalLocationPropertyBag


class SarifPhysicalLocation:
    def __init__(self, artifact_location, region, properties):
        """

        Args:
            artifact_location (SarifArtifactLocation):
            region (SarifRegion):
            properties (SarifPhysicalLocationPropertyBag):
        """
        self.artifactLocation = artifact_location
        self.region = region
        self.properties = properties

    def __str__(self):
        return f"SarifPhysicalLocation(" \
               f"artifact_location={self.artifactLocation}, " \
               f"region={self.region}" \
               f"properties={self.properties}"\
               f")"
