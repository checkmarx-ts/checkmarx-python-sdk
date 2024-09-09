from .CxSarifCategory import CxSarifCategory


class SarifTaxaPropertyBag:
    def __init__(self, tags, cx_cwe, cx_severity, cx_category, cx_query_group_name, cx_language_name,
                 cx_package_type_name, cx_stig_id, cx_stig_rule_id):
        """

        Args:
            tags (list of str):
            cx_cwe (str):
            cx_severity (str):
            cx_category (list of CxSarifCategory):
            cx_query_group_name (str):
            cx_language_name (str):
            cx_package_type_name (str):
            cx_stig_id (str):
            cx_stig_rule_id (str):
        """
        self.tags = tags
        self.cxCwe = cx_cwe
        self.cxSeverity = cx_severity
        self.cxCategory = cx_category
        self.cxQueryGroupName = cx_query_group_name
        self.cxLanguageName = cx_language_name
        self.cxPackageTypeName = cx_package_type_name
        self.cxStigID = cx_stig_id
        self.cxStigRuleID = cx_stig_rule_id

    def __str__(self):
        return f"SarifTaxaPropertyBag(" \
               f"tags={self.tags}, "\
               f"cx_cwe={self.cxCwe}, "\
               f"cx_severity={self.cxSeverity}, "\
               f"cx_category={self.cxCategory}, " \
               f"cx_query_group_name={self.cxQueryGroupName}, " \
               f"cx_language_name={self.cxLanguageName}, " \
               f"cx_package_type_name={self.cxPackageTypeName}, " \
               f"cx_stig_id={self.cxStigID}, " \
               f"cx_stig_rule_id={self.cxStigRuleID}" \
               f")"
