from dataclasses import dataclass


@dataclass
class Scanner:
    """

    Args:
        type (str): The type of scanner to run.
                Allowed values: sast sca kics apisec containers
        enable_auto_pull_requests (bool): If true, Checkmarx will automatically send suggested remediation actions.
                    Note: Relevant only for sca scanner.
        incremental_scan (bool): If true, an incremental scan will be run by default (unless extensive changes are
            identified in the project). Note: Relevant only for sast scans.
    """

    type: str = None
    enable_auto_pull_requests: bool = None
    incremental_scan: bool = None

    def to_dict(self):
        result = {"type": self.type}
        if self.enable_auto_pull_requests is not None:
            result.update({"enableAutoPullRequests": self.enable_auto_pull_requests})
        if self.incremental_scan is not None:
            result.update({"incrementalScan": self.incremental_scan})
        return result
