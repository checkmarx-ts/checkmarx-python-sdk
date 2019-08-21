# encoding: utf-8

import json


class CxDefineDataRetentionDateRangeRequest(object):
    """
    define data retention request
    """
    def __init__(self, start_date, end_date, duration_limit_in_hours):
        """

        :param start_date:
        :param end_date:
        :param duration_limit_in_hours:
        """
        self.start_date = start_date
        self.end_date = end_date
        self.duration_limit_in_hours = duration_limit_in_hours

    def get_post_data(self):
        return json.dumps(
            {
                "startDate": self.start_date,
                "endDate": self.end_date,
                "durationLimitInHours": self.duration_limit_in_hours
            }
        )