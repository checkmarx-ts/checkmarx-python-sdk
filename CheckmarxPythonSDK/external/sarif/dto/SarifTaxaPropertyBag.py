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
        self.Tags = tags
        self.CxCwe = cx_cwe
        self.CxSeverity = cx_severity
        self.CxCategory = cx_category
        self.CxQueryGroupName = cx_query_group_name
        self.CxLanguageName = cx_language_name
        self.CxPackageTypeName = cx_package_type_name
        self.CxStigID = cx_stig_id
        self.CxStigRuleID = cx_stig_rule_id

    def __str__(self):
        return f"SarifTaxaPropertyBag(" \
               f"tags={self.Tags}, "\
               f"cx_cwe={self.CxCwe}, "\
               f"cx_severity={self.CxSeverity}, "\
               f"cx_category={self.CxCategory}, " \
               f"cx_query_group_name={self.CxQueryGroupName}, " \
               f"cx_language_name={self.CxLanguageName}, " \
               f"cx_package_type_name={self.CxPackageTypeName}, " \
               f"cx_stig_id={self.CxStigID}, " \
               f"cx_stig_rule_id={self.CxStigRuleID}" \
               f")"
