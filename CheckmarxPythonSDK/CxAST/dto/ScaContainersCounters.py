class ScaContainersCounters(object):
    def __init__(self, total_packages_counter, total_vulnerabilities_counter, severity_vulnerabilities_counters,
                 state_vulnerabilities_counters, status_vulnerabilities_counters, age_vulnerabilities_counters,
                 package_vulnerabilities_counters):
        """

        Args:
            total_packages_counter (int):
            total_vulnerabilities_counter (int):
            severity_vulnerabilities_counters (list of dict):
            state_vulnerabilities_counters (list of dict):
            status_vulnerabilities_counters (list of dict):
            age_vulnerabilities_counters (list of dict):
            package_vulnerabilities_counters (list of dict):
        """
        self.totalPackagesCounter = total_packages_counter
        self.totalVulnerabilitiesCounter = total_vulnerabilities_counter
        self.severityVulnerabilitiesCounters = severity_vulnerabilities_counters
        self.stateVulnerabilitiesCounters = state_vulnerabilities_counters
        self.statusVulnerabilitiesCounters = status_vulnerabilities_counters
        self.ageVulnerabilitiesCounters = age_vulnerabilities_counters
        self.packageVulnerabilitiesCounters = package_vulnerabilities_counters

    def __str__(self):
        return """ScaContainersCounters(totalPackagesCounter={}, totalVulnerabilitiesCounter={},
        severityVulnerabilitiesCounters={}, stateVulnerabilitiesCounters={}, 
        statusVulnerabilitiesCounters={}, ageVulnerabilitiesCounters={},
        packageVulnerabilitiesCounters={})""".format(
            self.totalPackagesCounter, self.totalVulnerabilitiesCounter,
            self.severityVulnerabilitiesCounters, self.stateVulnerabilitiesCounters,
            self.statusVulnerabilitiesCounters, self.ageVulnerabilitiesCounters,
            self.packageVulnerabilitiesCounters
        )
