from .SarifDescription import SarifDescription


class SarifDriverRule:
    def __init__(self, rule_id, name, short_description, full_description, help_uri, help, relation_ships):
        """

        Args:
            rule_id (str):
            name (str):
            short_description (SarifDescription):
            full_description (SarifDescription):
            help_uri (str):
            help (SarifMultiFormatMessageString):
            relation_ships (SarifTaxaRelationship):
        """
        self.id = rule_id
        self.name = name
        self.helpUri = help_uri
        self.help = help
        self.fullDescription = full_description
        self.shortDescription = short_description
        self.relationships = relation_ships

    def __str__(self):
        return f"SarifDriverRule("\
               f"rule_id={self.id}, "\
               f"name={self.name}, "\
               f"help_uri={self.helpUri}, "\
               f"help={self.help}, "\
               f"full_description={self.fullDescription}, "\
               f"short_description={self.shortDescription}, "\
               f"relation_ships={self.relationships}"\
               ")"
