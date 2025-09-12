from dataclasses import dataclass


@dataclass
class AuditEvent:
    event_date: str = None
    event_type: str = None
    audit_resource: str = None
    action_type: str = None
    action_user_id: str = None
    ip_address: str = None
    data: dict = None


def construct_audit_event(item):
    return AuditEvent(
                event_date=item.get("eventDate"),
                event_type=item.get("eventType"),
                audit_resource=item.get("auditResource"),
                action_type=item.get("actionType"),
                action_user_id=item.get("actionUserId"),
                ip_address=item.get("ipAddress"),
                data=item.get("data")
            )
