# encoding: utf-8

import json


class CxDefineDataRetentionNumberOfScansRequest(object):
    """
    number of scans request
    """
    def __init__(self, number_of_successful_scans_to_preserve, duration_limit_in_hours):
        """

        :param number_of_successful_scans_to_preserve: int
        :param duration_limit_in_hours: int
        """
        self.number_of_successful_scans_to_preserve = number_of_successful_scans_to_preserve
        self.duration_limit_in_hours = duration_limit_in_hours

    def get_post_data(self):
        return json.dumps(
            {
                "numOfSuccessfulScansToPreserve": self.number_of_successful_scans_to_preserve,
                "durationLimitInHours": self.duration_limit_in_hours
            }
        )
