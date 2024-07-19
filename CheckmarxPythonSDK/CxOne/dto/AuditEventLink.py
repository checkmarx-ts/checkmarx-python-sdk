class AuditEventLink(object):

    def __init__(self, event_date, url, crc):
        """

        Args:
            event_date (str):
            url (str):
            crc (str):
        """
        self.event_date = event_date
        self.url = url
        self.crc = crc

    def __str__(self):
        return """AuditEventLink(event_date={}, url={}, crc={})""".format(
            self.event_date, self.url, self.crc
        )
