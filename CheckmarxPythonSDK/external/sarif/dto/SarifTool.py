from .SarifDriver import SarifDriver


class SarifTool:
    def __init__(self, driver):
        """

        Args:
            driver (SarifDriver):
        """
        self.driver = driver

    def __str__(self):
        return f"SarifDriver(" \
               f"driver={self.driver}"\
               f")"
