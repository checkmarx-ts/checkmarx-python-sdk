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
        self.Guid = guid
        self.Name = name
        self.FullDescription = full_description
        self.ShortDescription = short_description
        self.Taxa = taxa

    def __str__(self):
        return f"SarifTaxonomy(" \
               f"guid={self.Guid}, "\
               f"name={self.Name}, "\
               f"full_description={self.FullDescription}, "\
               f"short_description={self.ShortDescription}, "\
               f"taxa={self.Taxa}"\
               f")"
