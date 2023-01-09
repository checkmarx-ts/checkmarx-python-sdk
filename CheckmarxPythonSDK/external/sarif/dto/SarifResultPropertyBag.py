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
        self.Tags = tags
        self.SimilarityId = similarity_id
        self.CxCwe = cx_cwe
        self.CxStigID = cx_stig_id
        self.CxStigRuleID = cx_stig_rule_id

    def __str__(self):
        return f"SarifResultPropertyBag(" \
               f"tags={self.Tags}, "\
               f"similarity_id={self.SimilarityId}, " \
               f"cx_cwe={self.CxCwe}, " \
               f"cx_stig_id={self.CxStigID}, "\
               f"cx_stig_rule_id={self.CxStigRuleID}"\
               f")"
