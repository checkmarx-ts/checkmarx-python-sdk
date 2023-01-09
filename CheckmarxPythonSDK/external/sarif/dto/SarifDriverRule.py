from .SarifDescription import SarifDescription


class SarifDriverRule:
    def __init__(self, rule_id, name, short_description, full_description, help_uri, relation_ships):
        """

        Args:
            rule_id (str):
            name (str):
            short_description (SarifDescription):
            full_description (SarifDescription):
            help_uri (str):
            relation_ships (SarifTaxaRelationship):
        """
        self.ID = rule_id
        self.Name = name
        self.HelpURI = help_uri
        self.FullDescription = full_description
        self.ShortDescription = short_description
        self.Relationships = relation_ships

    def __str__(self):
        return f"SarifDriverRule("\
               f"rule_id={self.ID}, "\
               f"name={self.Name}, "\
               f"rule_help={self.HelpURI}, "\
               f"full_description={self.FullDescription}, "\
               f"short_description={self.ShortDescription}, "\
               f"relation_ships={self.Relationships}"\
               ")"
