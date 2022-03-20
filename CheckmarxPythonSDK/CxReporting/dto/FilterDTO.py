class FilterDTO(object):
    def __init__(self, filter_type, excluded_values=(), included_values=(), pattern=None):
        """

        Args:
            filter_type (int): maximum: 9   minimum: 1
                Filters to be applied in the report creation.
                Types of filters:
                    1 - Severity:
                        Build based on excludedValues.
                        If not defined, Low and Informative results are excluded by default.
                        Applicable for all report types.
                    2 - Result State:
                        Build based on excludedValues.
                        If not defined, none is excluded by default.
                        Applicable for all report types.
                    3 - Query/Vulnerability:
                        Build based on excludedValues.
                        If not defined none is excluded by default.
                        Applicable for the Scan Template only.
                    4 - Timeframe:
                        Build based on includedValues.
                        To define a date range composed by a starting and an ending date.
                        Applicable for all report types with the exception of the Scan Template.
                    5 - Status:
                        Build based on excludedValues.
                        If not defined, Resolved is excluded by default.
                        Applicable for all report types.
                    6 - Results Limit:
                        Build based on includedValues, 5000 is the default limit.
                        Applicable for the Scan Template only.
                    7 - Data Point:
                        Build based on includedValues.
                        By default last is used as data point.
                        Allowed values are last or first.
                        Applicable for all report types with the exception of the Scan Template.
                    8 - Project Name:
                        Build based on excludedValues.
                        If not defined none is excluded by default.
                        Applicable for Teams templates.
                    9 - Project Custom Fields:
                        Build based on includedValues.
                        If not defined no project is excluded by default.
                        Applicable for Teams and Application templates.
            excluded_values (list of str, optional):
            included_values (list of str, optional):
            pattern (str, optional):
        """
        if not isinstance(filter_type, int):
            raise ValueError("parameter filter_type type should be int")
        if excluded_values and not isinstance(excluded_values, (list, tuple)):
            raise ValueError("parameter excluded_values type should be list or tuple")
        if included_values and not isinstance(included_values, (list, tuple)):
            raise ValueError("parameter included_values type should be list or tuple")
        if pattern and not isinstance(pattern, str):
            raise ValueError("parameter pattern type should be str")

        self.type = filter_type
        self.excludedValues = excluded_values
        self.includedValues = included_values
        self.pattern = pattern

    def __str__(self):
        return """FilterDTO(type={}, excludedValues={}, includedValues={}, pattern={})""".format(
            self.type, self.excludedValues, self.includedValues, self.pattern
        )
