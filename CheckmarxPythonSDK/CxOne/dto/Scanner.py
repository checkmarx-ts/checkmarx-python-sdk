from dataclasses import dataclass


@dataclass
class Scanner:
    """

    Args:
        type (str): The type of scanner to run.
                Allowed values: sast sca kics apisec containers
        auto_pr_enabled (bool): If true, Checkmarx will automatically send suggested remediation actions.
                    Note: Relevant only for sca scanner.
        incremental (bool): If true, an incremental scan will be run by default (unless extensive changes are
            identified in the project). Note: Relevant only for sast scans.
    """

    type: str = None
    auto_pr_enabled: bool = None
    incremental: bool = None

    def to_dict(self):
        result = {"type": self.type}
        if self.auto_pr_enabled is not None:
            result.update({"autoPrEnabled": self.auto_pr_enabled})
        if self.incremental is not None:
            result.update({"incremental": self.incremental})
        return result
