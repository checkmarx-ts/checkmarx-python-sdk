class SourceNodeSummary(object):
    def __init__(self, source_node, count):
        """

        Args:
            source_node (str):
            count (int):
        """
        self.sourceNode = source_node
        self.count = count

    def __str__(self):
        return """SourceNodeSummary(sourceNode={}, count={})""".format(
            self.sourceNode, self.count
        )
