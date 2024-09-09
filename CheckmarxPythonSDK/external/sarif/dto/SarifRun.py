from .SarifTool import SarifTool
from .SarifScanResult import SarifScanResult
from .SarifTaxonomy import SarifTaxonomy


class SarifRun:

    def __init__(self, tool, results, taxonomies):
        """

        Args:
            tool (SarifTool):
            results (list of SarifScanResult):
            taxonomies (list of SarifTaxonomy)
        """
        self.tool = tool
        self.results = results
        self.taxonomies = taxonomies

    def __str__(self):
        return f"SarifRun(" \
               f"tool={self.tool}, "\
               f"results={self.results}"\
               f"taxonomies={self.taxonomies}"\
               f")"
