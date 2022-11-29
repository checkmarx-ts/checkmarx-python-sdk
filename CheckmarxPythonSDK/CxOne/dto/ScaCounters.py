class ScaCounters(object):
    """Counters of KICS Engine."""
    def __init__(self, severity_counters, status_counters, state_counters, severity_status_counters,
                 source_file_counters, age_counters, total_counter, file_scanned_counter):
        """

        Args:
            severity_counters (list of dict): array of the result count grouped by severity.
            status_counters (list of dict): array of the result count grouped by status.
            state_counters (list of dict): array of the counters grouped by state. will be included only if the
                                apply-predicates parameter is true
            severity_status_counters (list of dict): array of the counters grouped by severity and status.
                            will be included only if the include-severity-status parameter is true.
                            NOTICE: will not contain FIXED status.
            source_file_counters (list of dict): array of the result count grouped by code source file.
            age_counters (list of dict): array of the result count grouped by age.
            total_counter (int): Total number of results
            file_scanned_counter (int):
        """
        self.severityCounters = severity_counters
        self.statusCounters = status_counters
        self.stateCounters = state_counters
        self.severityStatusCounters = severity_status_counters
        self.sourceFileCounters = source_file_counters
        self.ageCounters = age_counters
        self.totalCounter = total_counter
        self.filesScannedCounter = file_scanned_counter

    def __str__(self):
        return """ScaCounters(severityCounters={}, statusCounters={}, stateCounters={}, severityStatusCounters={}
        sourceFileCounters={}, ageCounters={}, totalCounter={}, filesScannedCounter={})""".format(
            self.severityCounters, self.statusCounters, self.stateCounters, self.severityStatusCounters,
            self.sourceFileCounters, self.ageCounters, self.totalCounter, self.filesScannedCounter
        )
