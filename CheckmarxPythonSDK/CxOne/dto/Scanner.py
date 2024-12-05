class Scanner(object):

    def __init__(self,
                 scanner_type: str,
                 auto_pr_enabled: bool = None,
                 incremental: bool = None
                 ):
        """

        Args:
            scanner_type (str): The type of scanner to run.
                    Allowed values: sast sca kics apisec containers
            auto_pr_enabled (bool): If true, Checkmarx will automatically send suggested remediation actions.
                        Note: Relevant only for sca scanner.
            incremental (bool): If true, an incremental scan will be run by default (unless extensive changes are
                identified in the project). Note: Relevant only for sast scans.
        """
        self.type = scanner_type
        self.autoPrEnabled = auto_pr_enabled
        self.incremental = incremental

    def __str__(self):
        return f"Scanner(type={self.type}, autoPrEnabled={self.autoPrEnabled}, incremental={self.incremental})"

    def to_dict(self):
        result = {"type": self.type}
        if self.autoPrEnabled is not None:
            result.update({"enableAutoPullRequests": self.autoPrEnabled})
        if self.incremental is not None:
            result.update({"incrementalScan": self.incremental})
        return result
