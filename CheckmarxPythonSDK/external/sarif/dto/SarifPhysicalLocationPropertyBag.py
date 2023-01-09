class SarifPhysicalLocationPropertyBag:
    def __init__(self, tags, snippet):
        """

        Args:
            tags (list of str):
            snippet (str):
        """
        self.Tags = tags
        self.Snippet = snippet

    def __str__(self):
        return f"SarifPhysicalLocationPropertyBag(" \
               f"tags={self.Tags}, "\
               f"snippet={self.Snippet}"\
               f")"
