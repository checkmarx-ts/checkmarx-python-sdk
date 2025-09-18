from dataclasses import dataclass


@dataclass
class ScanConfig:
    """

    Args:
        type (str): The type of scanners run on the scan.
                Enum: [ sca, sast, kics, system ]
        value (dict): An object representing the configuration in a key-value format. Relevant only for SAST scans.
                example:  { "incremental": "true", "presetName": "Default" }
    """
    type: str = None
    value: dict = None

    def to_dict(self):
        if self.value:
            return {
                "type": self.type,
                "value": self.value,
            }
        return {
            "type": self.type
        }
