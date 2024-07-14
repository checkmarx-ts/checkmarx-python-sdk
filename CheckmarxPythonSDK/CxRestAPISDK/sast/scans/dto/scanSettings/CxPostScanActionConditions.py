class CxPostScanActionConditions(object):

    def __init__(self, run_only_when_new_results, run_only_when_new_results_min_severity):
        """

        Args:
            run_only_when_new_results (bool):
            run_only_when_new_results_min_severity (int):
        """
        self.run_only_when_new_results = run_only_when_new_results
        self.run_only_when_new_results_min_severity = run_only_when_new_results_min_severity

    def __str__(self):
        return ("CxPostScanActionConditions(run_only_when_new_results={}, "
                "run_only_when_new_results_min_severity={})").format(
            self.run_only_when_new_results, self.run_only_when_new_results_min_severity
        )
