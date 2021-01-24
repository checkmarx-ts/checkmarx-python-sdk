class CxScanResultAttackVector(object):

    def __init__(self, result_id, best_fix_location_node, nodes):
        """

        Args:
            result_id (str):
            best_fix_location_node (int):
            nodes (`list` of `CxScanResultNode`):
        """
        self.result_id = result_id
        self.best_fix_location_node = best_fix_location_node
        self.nodes = nodes

    def __str__(self):
        return """CxScanResultAttackVector(result_id={}, best_fix_location_node={}, nodes={})""".format(
            self.result_id, self.best_fix_location_node, self.nodes
        )
