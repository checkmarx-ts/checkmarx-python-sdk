# encoding: utf-8


class CxOsaSummaryReport(object):
    """
    osa report
    """

    def __init__(self, total_libraries, high_vulnerability_libraries, medium_vulnerability_libraries,
                 low_vulnerability_libraries, non_vulnerable_libraries, vulnerable_and_updated,
                 vulnerable_and_outdated, vulnerability_score, total_high_vulnerabilities, total_medium_vulnerabilities,
                 total_low_vulnerabilities):
        """

        Args:
            total_libraries (str):
            high_vulnerability_libraries (str):
            medium_vulnerability_libraries (str):
            low_vulnerability_libraries (str):
            non_vulnerable_libraries (str):
            vulnerable_and_updated (str):
            vulnerable_and_outdated (str):
            vulnerability_score (str):
            total_high_vulnerabilities (str):
            total_medium_vulnerabilities (str):
            total_low_vulnerabilities (str):


        """
        self.total_libraries = total_libraries
        self.high_vulnerability_libraries = high_vulnerability_libraries
        self.medium_vulnerability_libraries = medium_vulnerability_libraries
        self.low_vulnerability_libraries = low_vulnerability_libraries
        self.non_vulnerable_libraries = non_vulnerable_libraries
        self.vulnerable_and_updated = vulnerable_and_updated
        self.vulnerable_and_outdated = vulnerable_and_outdated
        self.vulnerability_score = vulnerability_score
        self.total_high_vulnerabilities = total_high_vulnerabilities
        self.total_medium_vulnerabilities = total_medium_vulnerabilities
        self.total_low_vulnerabilities = total_low_vulnerabilities

    def __str__(self):
        return """CxOsaReport(total_libraries={}, high_vulnerability_libraries={}, medium_vulnerability_libraries={},
                 low_vulnerability_libraries={}, non_vulnerable_libraries={}, vulnerable_and_updated={},
                 vulnerable_and_outdated={}, vulnerability_score={}, total_high_vulnerabilities={}, 
                 total_medium_vulnerabilities={}, total_low_vulnerabilities={})""".format(
            self.total_libraries, self.high_vulnerability_libraries, self.medium_vulnerability_libraries,
            self.low_vulnerability_libraries, self.non_vulnerable_libraries, self.vulnerable_and_updated,
            self.vulnerable_and_outdated, self.vulnerability_score, self.total_high_vulnerabilities,
            self.total_medium_vulnerabilities, self.total_low_vulnerabilities
        )
