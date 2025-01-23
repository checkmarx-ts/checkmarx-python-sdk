# encoding: utf-8

import json


class CxDefineDataRetentionNumberOfScansRequest(object):
    """
    number of scans request
    """
    def __init__(self, number_of_successful_scans_to_preserve, duration_limit_in_hours):
        """

        Args:
            number_of_successful_scans_to_preserve (int):
            duration_limit_in_hours (int):
        """
        self.number_of_successful_scans_to_preserve = number_of_successful_scans_to_preserve
        self.duration_limit_in_hours = duration_limit_in_hours

    def to_dict(self):
        return {
                "numOfSuccessfulScansToPreserve": self.number_of_successful_scans_to_preserve,
                "durationLimitInHours": self.duration_limit_in_hours
            }

    def __str__(self):
        return """CxDefineDataRetentionNumberOfScansRequest(number_of_successful_scans_to_preserve={},
         duration_limit_in_hours={})""".format(
            self.number_of_successful_scans_to_preserve, self.duration_limit_in_hours
        )
