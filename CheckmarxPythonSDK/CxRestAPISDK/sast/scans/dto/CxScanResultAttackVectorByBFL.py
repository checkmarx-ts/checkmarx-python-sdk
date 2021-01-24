class CxScanResultAttackVectorByBFL(object):
    def __init__(self, scan_id, query_version_code, best_fix_location_node, attack_vectors):
        """

        Args:
            scan_id (int):
            query_version_code (int):
            best_fix_location_node (`CxScanResultNode`):
            attack_vectors (`list` of `CxScanResultAttackVector`):
        """
        self.scan_id = scan_id
        self.query_version_code = query_version_code
        self.best_fix_location_node = best_fix_location_node
        self.attack_vectors = attack_vectors

    def __str__(self):
        return """CxScanResultAttackVectorByBFL(scan_id={}, query_version_code={}, best_fix_location_node={}, 
        attack_vectors={})""".format(
            self.scan_id, self.query_version_code, self.best_fix_location_node, self.attack_vectors
        )
