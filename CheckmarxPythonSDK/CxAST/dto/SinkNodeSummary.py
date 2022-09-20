class SinkNodeSummary(object):
    def __init__(self, sink_node, count):
        """

        Args:
            sink_node (str):
            count (int):
        """
        self.sinkNode = sink_node
        self.count = count

    def __str__(self):
        return """SinkNodeSummary(sinkNode={}, count={})""".format(
            self.sinkNode, self.count
        )
