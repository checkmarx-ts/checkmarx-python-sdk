class ApiSecCounters(object):
    def __init__(self, severity_counters, status_counters, state_counters, severity_status_counters,
                 source_file_counters, age_counters, total_counter, files_scanned_counter):
        """

        Args:
            severity_counters (list of dict):
            status_counters (dict):
            state_counters (list of dict):
            severity_status_counters (dict):
            source_file_counters (dict):
            age_counters (dict):
            total_counter (int):
            files_scanned_counter (int):
        """
        self.severityCounters = severity_counters
        self.statusCounters = status_counters
        self.stateCounters = state_counters
        self.severityStatusCounters = severity_status_counters
        self.sourceFileCounters = source_file_counters
        self.ageCounters = age_counters
        self.totalCounter = total_counter
        self.filesScannedCounter = files_scanned_counter

    def __str__(self):
        return """ApiSecCounters(severityCounters={}, statusCounters={}, stateCounters={},
        severityStatusCounters={}, sourceFileCounters={}, ageCounters={}, totalCounter={}, 
        filesScannedCounter={})""".format(
            self.severityCounters, self.statusCounters, self.stateCounters,
            self.severityStatusCounters, self.sourceFileCounters, self.ageCounters, self.totalCounter,
            self.filesScannedCounter
        )
