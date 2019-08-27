# encoding: utf-8

import json


class CxSchedulingSettings(object):
    """
    scheduling settings
    """
    def __init__(self, schedule_type, schedule_days, schedule_time):
        """

        Args:
            schedule_type (str):
            schedule_days (:obj:`list` of :obj:`str`):
            schedule_time (str):
        """
        self.schedule_type = schedule_type
        self.schedule_days = schedule_days
        self.schedule_time = schedule_time

    def get_post_data(self):
        return json.dumps(
            {
                "scheduleType": self.schedule_type,
                "scheduledDays": list(self.schedule_days),
                "scheduleTime": self.schedule_time
            }
        )

    def __str__(self):
        return "CxSchedulingSettings(schedule_type={}, schedule_days={}, schedule_time={})".format(
            self.schedule_type, self.schedule_days, self.schedule_time
        )
