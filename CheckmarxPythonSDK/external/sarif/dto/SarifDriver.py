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
        self.Name = name
        self.FullName = full_name
        self.Version = version
        self.InformationURI = information_uri
        self.Rules = rules

    def __str__(self):
        return f"SarifDriver(" \
               f"name={self.Name}, " \
               f"full_name={self.FullName}, " \
               f"version={self.Version}, " \
               f"information_uri={self.InformationURI}, " \
               f"rules={self.Rules}"\
               f")"
