from .httpRequests import get_request
from .utilities import type_check
from .dto import (
    AuditEvent,
    AuditEventLink,
    AuditEvents,
)

api_url = "/api/audit"


def __construct_audit_events(audit_events):
    return AuditEvents(
        links=[
            AuditEventLink(
                event_date=link.get("eventDate"),
                url=link.get("url"),
                crc=link.get("crc"),
            ) for link in audit_events.get("links", [])
               ],
        events=[
            AuditEvent(
                event_date=event.get("eventDate"),
                event_type=event.get("eventType"),
                audit_resource=event.get("auditResource"),
                action_type=event.get("actionType"),
                action_user_id=event.get("actionUserId"),
                ip_address=event.get("ipAddress"),
                data=event.get("data")
            ) for event in audit_events.get("events", [])
        ],
    )


def get_audit_events_for_tenant(offset=0, limit=200):
    """

    Args:
        offset (int): The number of items to skip before starting to collect the result set
                    Default value : 0
        limit (int):  The number of items to return
                    Default value : 20

    Returns:
        `ApplicationsCollection`
    """
    type_check(offset, int)
    type_check(limit, int)
    relative_url = api_url + "?offset={offset}&limit={limit}".format(offset=offset, limit=limit)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return __construct_audit_events(audit_events=item)
