class ScaPackageCounters(object):
    def __init__(self, severity_counters, status_counters, state_counters, severity_status_counters,
                 source_file_counters, age_counters, total_counter, files_scanned_counter, outdated_counter,
                 risk_level_counters, license_counters, package_counters):
        """

        Args:
            severity_counters (list of dict):
            status_counters (list of dict):
            state_counters (list of dict):
            severity_status_counters (list of dict):
            source_file_counters (list of dict):
            age_counters (list of dict):
            total_counter (int):
            files_scanned_counter (int):
            outdated_counter (int):
            risk_level_counters (list of dict):
            license_counters (list of dict):
            package_counters (list of dict):
        """
        self.severityCounters = severity_counters
        self.statusCounters = status_counters
        self.stateCounters = state_counters
        self.severityStatusCounters = severity_status_counters
        self.sourceFileCounters = source_file_counters
        self.ageCounters = age_counters
        self.totalCounter = total_counter
        self.filesScannedCounter = files_scanned_counter
        self.outdatedCounter = outdated_counter
        self.riskLevelCounters = risk_level_counters
        self.licenseCounters = license_counters
        self.packageCounters = package_counters

    def __str__(self):
        return """ScaPackageCounters(severityCounters={}, statusCounters={}, stateCounters={}, 
        severityStatusCounters={}, sourceFileCounters={}, ageCounters={}, totalCounter={}, filesScannedCounter={},
        outdatedCounter={}, riskLevelCounters={}, licenseCounters={}, packageCounters={})""".format(
            self.severityCounters, self.statusCounters, self.stateCounters,
            self.severityStatusCounters, self.sourceFileCounters, self.ageCounters, self.totalCounter,
            self.filesScannedCounter, self.outdatedCounter, self.riskLevelCounters, self.licenseCounters,
            self.packageCounters
        )
