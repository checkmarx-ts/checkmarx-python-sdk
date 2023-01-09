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
        self.ArtifactLocation = artifact_location
        self.Region = region
        self.Properties = properties

    def __str__(self):
        return f"SarifPhysicalLocation(" \
               f"artifact_location={self.ArtifactLocation}, " \
               f"region={self.Region}" \
               f"properties={self.Properties}"\
               f")"
