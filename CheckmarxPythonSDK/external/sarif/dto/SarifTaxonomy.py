from .SarifTaxa import SarifTaxa
from .SarifDescription import SarifDescription


class SarifTaxonomy:
    def __init__(self, guid, name, full_description, short_description, taxa):
        """

        Args:
            guid (str):
            name (str):
            full_description (SarifDescription):
            short_description (SarifDescription):
            taxa (list of SarifTaxa):
        """
        self.guid = guid
        self.name = name
        self.fullDescription = full_description
        self.shortDescription = short_description
        self.taxa = taxa

    def __str__(self):
        return f"SarifTaxonomy(" \
               f"guid={self.guid}, "\
               f"name={self.name}, "\
               f"full_description={self.fullDescription}, "\
               f"short_description={self.shortDescription}, "\
               f"taxa={self.taxa}"\
               f")"
