# encoding: utf-8


class CxStatisticsResult(object):
    """
    statistics result
    """

    def __init__(
        self,
        critical_severity=None,
        high_severity=None,
        medium_severity=None,
        low_severity=None,
        info_severity=None,
        statistics_calculation_date=None,
    ):
        """

        Args:
            critical_severity (int):
            high_severity (int):
            medium_severity (int):
            low_severity (int):
            info_severity (int):
            statistics_calculation_date (str):
        """
        self.critical_severity = critical_severity
        self.high_severity = high_severity
        self.medium_severity = medium_severity
        self.low_severity = low_severity
        self.info_severity = info_severity
        self.statistics_calculation_date = statistics_calculation_date

    @classmethod
    def from_dict(cls, item: dict) -> "CxStatisticsResult":
        return cls(
            critical_severity=item.get("criticalSeverity"),
            high_severity=item.get("highSeverity"),
            medium_severity=item.get("mediumSeverity"),
            low_severity=item.get("lowSeverity"),
            info_severity=item.get("infoSeverity"),
            statistics_calculation_date=item.get("statisticsCalculationDate"),
        )

    def __str__(self):
        return """CxStatisticsResult(
                    critical_severity: {},
                    high_severity: {}, 
                    medium_severity: {}, 
                    low_severity: {}, 
                    info_severity:{},
                    statistics_calculation_date:{}
                  )""".format(
            self.critical_severity,
            self.high_severity,
            self.medium_severity,
            self.low_severity,
            self.info_severity,
            self.statistics_calculation_date,
        )
