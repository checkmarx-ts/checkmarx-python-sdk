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
        self.Tool = tool
        self.Results = results
        self.Taxonomies = taxonomies

    def __str__(self):
        return f"SarifRun(" \
               f"tool={self.Tool}, "\
               f"results={self.Results}"\
               f"taxonomies={self.Taxonomies}"\
               f")"
