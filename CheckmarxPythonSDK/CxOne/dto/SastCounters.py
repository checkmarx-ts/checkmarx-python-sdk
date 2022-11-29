class SastCounters(object):
    """Counters of SAST Engine."""
    def __init__(self, severity_counters=None, status_counters=None, state_counters=None, severity_status_counters=None,
                 source_file_counters=None, age_counters=None, total_counter=None, queries_counters=None, sink_file_counters=None,
                 language_counters=None, compliance_counters=None, file_scanned_counter=None):
        """

        Args:
            queries_counters (list of dict): array of the counters grouped by query name.
                                        will be included only if the include-queries parameter is true.
            sink_file_counters (list of dict): array of the result count grouped by code sink file.
            language_counters (list of dict): array of the result count grouped by language.
            compliance_counters (list of dict): array of the result count grouped by compliance
            severity_counters (list of dict): array of the result count grouped by severity.
            status_counters (list of dict): array of the result count grouped by status.
            state_counters (list of dict): array of the counters grouped by state. will be included only if the
                        apply-predicates parameter is true
            severity_status_counters (list of dict): array of the counters grouped by severity and status. will be
                        included only if the include-severity-status parameter is true.
                        NOTICE: will not contain FIXED status.
            source_file_counters (list of dict): array of the result count grouped by code source file.
            age_counters (list of dict): array of the result count grouped by age.
            total_counter (int): Total number of results
            file_scanned_counter (int):
        """
        self.queriesCounters = queries_counters
        self.sinkFileCounters = sink_file_counters
        self.languageCounters = language_counters
        self.complianceCounters = compliance_counters
        self.severityCounters = severity_counters
        self.statusCounters = status_counters
        self.stateCounters = state_counters
        self.severityStatusCounters = severity_status_counters
        self.sourceFileCounters = source_file_counters
        self.ageCounters = age_counters
        self.totalCounter = total_counter
        self.filesScannedCounter = file_scanned_counter

    def __str__(self):
        return """SastCounters(queriesCounters={}, sinkFileCounters={}, languageCounters={}, 
        complianceCounters={}, severityCounters={}, statusCounters={}, stateCounters={},
        severityStatusCounters={}, sourceFileCounters={}, ageCounters={}, totalCounter={},
        filesScannedCounter={})""".format(
            self.queriesCounters, self.sinkFileCounters, self.languageCounters, self.complianceCounters,
            self.severityCounters, self.statusCounters, self.stateCounters, self.severityStatusCounters,
            self.sourceFileCounters, self.ageCounters, self.totalCounter, self.filesScannedCounter
        )
