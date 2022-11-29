class KicsCounters(object):
    """Counters of KICS Engine"""
    def __init__(self, age_counters, category_summary, files_scanned_counter, platform_summary, severity_counters,
                 severity_status_counters, state_counters, status_counters, total_counter, source_file_counters):
        """

        Args:
            severity_counters (list of dict): array of the result count grouped by severity.
            status_counters (list of dict): array of the result count grouped by status.
            state_counters (list of dict): array of the counters grouped by state.
                            will be included only if the apply-predicates parameter is true
            severity_status_counters (list of dict): array of the counters grouped by severity and status.
                            will be included only if the include-severity-status parameter is true.
                            NOTICE: will not contain FIXED status.
            source_file_counters (list of dict):
            age_counters (list of dict): array of the result count grouped by age.
            total_counter (int): Total number of results
            files_scanned_counter (int): Number of files scanned
            platform_summary (list of dict): array of the result count grouped by platform.
            category_summary (list of dict): array of the result count grouped by category.
        """
        self.ageCounters = age_counters
        self.categorySummary = category_summary
        self.filesScannedCounter = files_scanned_counter
        self.platformSummary = platform_summary
        self.severityCounters = severity_counters
        self.severityStatusCounters = severity_status_counters
        self.stateCounters = state_counters
        self.statusCounters = status_counters
        self.totalCounter = total_counter
        self.sourceFileCounters = source_file_counters

    def __str__(self):
        return """KicsCounters(ageCounters={}, categorySummary={}, filesScannedCounter={}, platformSummary={}
        severityCounters={}, severityStatusCounters={}, stateCounters={}, statusCounters={}, 
        totalCounter={}, sourceFileCounters={})""".format(
            self.ageCounters, self.categorySummary, self.filesScannedCounter, self.platformSummary,
            self.severityCounters, self.severityStatusCounters, self.stateCounters, self.statusCounters,
            self.totalCounter, self.sourceFileCounters
        )
