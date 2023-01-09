from .SarifPhysicalLocation import SarifPhysicalLocation


class SarifLocation:
    def __init__(self, physical_location):
        """

        Args:
            physical_location (SarifPhysicalLocation):
        """
        self.PhysicalLocation = physical_location

    def __str__(self):
        return f"SarifLocation(" \
               f"physical_location={self.PhysicalLocation}, " \
               f")"
