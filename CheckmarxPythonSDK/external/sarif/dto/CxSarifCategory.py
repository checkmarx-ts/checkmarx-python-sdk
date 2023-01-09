class CxSarifCategory:
    def __init__(self, cx_category_name, cx_category_type):
        """

        Args:
            cx_category_name (str):
            cx_category_type (str):
        """
        self.CxCategoryName = cx_category_name
        self.CxCategoryType = cx_category_type

    def __str__(self):
        return f"CxSarifCategory(" \
               f"cx_category_name={self.CxCategoryName}, "\
               f"cx_category_type={self.CxCategoryType}"\
               f")"
