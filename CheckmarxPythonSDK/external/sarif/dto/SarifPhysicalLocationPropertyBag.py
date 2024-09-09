class SarifPhysicalLocationPropertyBag:
    def __init__(self, tags, snippet):
        """

        Args:
            tags (list of str):
            snippet (str):
        """
        self.tags = tags
        self.snippet = snippet

    def __str__(self):
        return f"SarifPhysicalLocationPropertyBag(" \
               f"tags={self.tags}, "\
               f"snippet={self.snippet}"\
               f")"
