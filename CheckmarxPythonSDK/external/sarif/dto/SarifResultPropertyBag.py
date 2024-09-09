class SarifResultPropertyBag:
    def __init__(self, tags, similarity_id, cx_cwe, cx_stig_id, cx_stig_rule_id):
        """

        Args:
            tags (list of str):
            similarity_id (int):
            cx_cwe (str):
            cx_stig_id (str):
            cx_stig_rule_id (str):
        """
        self.tags = tags
        self.similarityId = similarity_id
        self.cxCwe = cx_cwe
        self.cxStigID = cx_stig_id
        self.cxStigRuleID = cx_stig_rule_id

    def __str__(self):
        return f"SarifResultPropertyBag(" \
               f"tags={self.tags}, "\
               f"similarity_id={self.similarityId}, " \
               f"cx_cwe={self.cxCwe}, " \
               f"cx_stig_id={self.cxStigID}, "\
               f"cx_stig_rule_id={self.cxStigRuleID}"\
               f")"
