from .SarifTaxaPropertyBag import SarifTaxaPropertyBag
from .SarifDescription import SarifDescription


class SarifTaxa:
    def __init__(self, taxa_id, name, full_description, short_description, properties):
        """

        Args:
            taxa_id (str):
            name (str):
            full_description (SarifDescription):
            short_description (SarifDescription):
            properties (SarifTaxaPropertyBag):
        """
        self.id = taxa_id
        self.name = name
        self.fullDescription = full_description
        self.shortDescription = short_description
        self.properties = properties

    def __str__(self):
        return f"SarifTaxa(" \
               f"taxa_id={self.id}, "\
               f"name={self.name}, "\
               f"full_description={self.fullDescription}, "\
               f"short_description={self.shortDescription}, "\
               f"properties={self.properties}"\
               f")"
