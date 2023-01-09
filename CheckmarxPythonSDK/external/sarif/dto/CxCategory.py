class CxCategory:
    def __init__(self, query_id, name, cwe, severity, category_name, category_type, query_group_name, language_name,
                 package_type_name):
        """

        Args:
            query_id (int):
            name (str):
            cwe (int):
            severity (int):
            category_name (str):
            category_type (str):
            query_group_name (str):
            language_name (str):
            package_type_name (str):
        """
        self.QueryId = query_id
        self.Name = name
        self.Cwe = cwe
        self.Severity = severity,
        self.CategoryName = category_name
        self.CategoryType = category_type
        self.QueryGroupName = query_group_name
        self.LanguageName = language_name
        self.PackageTypeName = package_type_name

    def __str__(self):
        return f"CxCategory(" \
               f"query_id={self.QueryId}, " \
               f"name={self.Name}, "\
               f"cwe={self.Cwe}, "\
               f"severity={self.Severity}, "\
               f"category_name={self.CategoryName}, "\
               f"category_type={self.CategoryType}, "\
               f"query_group_name={self.QueryGroupName}, "\
               f"language_name={self.LanguageName}, " \
               f"package_type_name={self.PackageTypeName}, " \
               f")"
