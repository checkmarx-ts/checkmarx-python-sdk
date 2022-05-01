# encoding: utf-8
class ScanConfig(object):
    def __init__(self, scan_type, value=None):
        """

        Args:
            scan_type (str): The type of scanners run on the scan.
                    Enum: [ sca, sast, kics, system ]
            value (dict): An object representing the configuration in a key-value format. Relevant only for SAST scans.
                    example:  { "incremental": "true", "presetName": "Default" }
        """
        self.type = scan_type
        self.value = value

    def __str__(self):
        return """ScanConfig(type={}, value={})""".format(
            self.type, self.value
        )

    def as_dict(self):
        if not self.value:
            return {
                "type": self.type,
                "value": self.value,
            }
        return {
            "type": self.type
        }
