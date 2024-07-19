from .AuditEventLink import AuditEventLink
from .AuditEvent import AuditEvent


class AuditEvents(object):

    def __init__(self, links, events):
        """

        Args:
            links (list of AuditEventLink):
            events (list of AuditEvent):
        """
        self.links = links
        self.events = events

    def __str__(self):
        return """AuditEvents(links={}, events={})""".format(
            self.links, self.events
        )
