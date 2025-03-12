# encoding: utf-8
class StatusDetails(object):
    def __init__(self, name, status, details, start_date, end_date):
        """

        Args:
            name:
            status:
            details:
        """
        self.name = name
        self.status = status
        self.details = details
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return (f"StatusDetails("
                f"name={self.name}, "
                f"status={self.status}, "
                f"details={self.details}, "
                f"start_date={self.start_date}), "
                f"end_date={self.end_date}")

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
