from .SarifDriverRule import SarifDriverRule


class SarifDriver:

    def __init__(self, name, version, information_uri, rules, full_name=None):
        """

        Args:
            name (str):
            full_name (str):
            version (str):
            information_uri (str):
            rules (list of SarifDriverRule):
        """
        self.name = name
        self.fullName = full_name
        self.version = version
        self.informationUri = information_uri
        self.rules = rules

    def __str__(self):
        return f"SarifDriver(" \
               f"name={self.name}, " \
               f"full_name={self.fullName}, " \
               f"version={self.version}, " \
               f"information_uri={self.informationUri}, " \
               f"rules={self.rules}"\
               f")"
