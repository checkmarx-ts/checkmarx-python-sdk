from .SarifMessage import SarifMessage
from .SarifResultPropertyBag import SarifResultPropertyBag
from .SarifLocation import SarifLocation


class SarifScanResult:
    def __init__(self, rule_id, kind, level, message, properties, locations):
        """

        Args:
            rule_id (str):
            kind (str):
            level (str):
            message (SarifMessage):
            properties (SarifResultPropertyBag):
            locations (list of SarifLocation):
        """
        self.RuleID = rule_id
        self.Kind = kind
        self.Level = level
        self.Message = message
        self.Properties = properties
        self.Locations = locations

    def __str__(self):
        return f"SarifScanResult(" \
               f"rule_id={self.RuleID}, "\
               f"kind={self.Kind}, " \
               f"level={self.Level}, " \
               f"message={self.Message}, " \
               f"properties={self.Properties}, "\
               f"locations={self.Locations}"\
               f")"
