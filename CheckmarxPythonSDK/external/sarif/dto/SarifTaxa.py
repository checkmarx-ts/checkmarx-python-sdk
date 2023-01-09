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
        self.Id = taxa_id
        self.Name = name
        self.FullDescription = full_description
        self.ShortDescription = short_description
        self.Properties = properties

    def __str__(self):
        return f"SarifTaxa(" \
               f"taxa_id={self.Id}, "\
               f"name={self.Name}, "\
               f"full_description={self.FullDescription}, "\
               f"short_description={self.ShortDescription}, "\
               f"properties={self.Properties}"\
               f")"
