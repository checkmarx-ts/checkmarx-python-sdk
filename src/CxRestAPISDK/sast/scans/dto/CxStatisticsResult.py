# encoding: utf-8


class CxStatisticsResult(object):
    """
    statistics result
    """

    def __init__(self, high_severity=None, medium_severity=None, low_severity=None, info_severity=None,
                 statistics_calculation_date=None):
        """

        :param high_severity: int
        :param medium_severity: int
        :param low_severity: int
        :param info_severity: int
        :param statistics_calculation_date: str
        """
        self.high_severity = high_severity
        self.medium_severity = medium_severity
        self.low_severity = low_severity
        self.info_severity = info_severity
        self.statistics_calculation_date = statistics_calculation_date
