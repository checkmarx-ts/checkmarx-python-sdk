class BflTree(object):
    def __init__(self, tree_id, bfl, results, additional_properties):
        """

        Args:
            tree_id (str): tree ID in the forest
            bfl (ResultNode): Best Fix Location node of the tree
            results (list of Result): results for the BFL node
            additional_properties (dict): the additional properties will be added if include-graph is set to true
        """
        self.id = tree_id
        self.bfl = bfl
        self.results = results
        self.additionalProperties = additional_properties

    def __str__(self):
        return """BflTree(id={}, bfl={}, results={}, additionalProperties={})""".format(
            self.id, self.bfl, self.results, self.additionalProperties
        )
