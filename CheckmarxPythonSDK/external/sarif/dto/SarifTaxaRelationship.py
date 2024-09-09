class SarifTaxaRelationship:
    def __init__(self, target):
        """

        Args:
            target (SarifTaxaRelationshipTarget):
        """
        self.target = target

    def __str__(self):
        return f"SarifTaxaRelationship(" \
               f"target={self.target}"\
               f")"
