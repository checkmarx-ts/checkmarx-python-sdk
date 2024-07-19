class AuditEvent(object):

    def __init__(self, event_date, event_type, audit_resource, action_type, action_user_id, ip_address, data):
        """

        Args:
            event_date (str):
            event_type (str):
            audit_resource (str):
            action_type (str):
            action_user_id (str):
            ip_address (str):
            data (dict):
        """
        self.event_date = event_date
        self.event_type = event_type
        self.audit_resource = audit_resource
        self.action_type = action_type
        self.action_user_id = action_user_id
        self.ip_address = ip_address
        self.data = data

    def __str__(self):
        return """AuditEvent(event_date={}, event_type={}, audit_resource={}, action_type={}, action_user_id={}, 
        ip_address={}, data={})""".format(
            self.event_date, self.event_type, self.audit_resource, self.action_type, self.action_user_id,
            self.ip_address, self.data
        )
