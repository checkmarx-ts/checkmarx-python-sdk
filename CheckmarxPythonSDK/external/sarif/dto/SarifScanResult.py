from .SarifMessage import SarifMessage
from .SarifResultPropertyBag import SarifResultPropertyBag
from .SarifLocation import SarifLocation


class SarifScanResult:
    def __init__(self, rule_id, kind, level, message, properties, locations, fixes):
        """

        Args:
            rule_id (str):
            kind (str):
            level (str):
            message (SarifMessage):
            properties (SarifResultPropertyBag):
            locations (list of SarifLocation):
            fixes ():
        """
        self.ruleId = rule_id
        self.kind = kind
        self.level = level
        self.message = message
        self.properties = properties
        self.locations = locations
        self.fixes = fixes

    def __str__(self):
        return f"SarifScanResult(" \
               f"rule_id={self.ruleId}, "\
               f"kind={self.kind}, " \
               f"level={self.level}, " \
               f"message={self.message}, " \
               f"properties={self.properties}, "\
               f"locations={self.locations}, "\
               f"fixes={self.fixes}, "\
               f")"
