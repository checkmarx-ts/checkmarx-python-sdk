from .Property import Property


class SastScan(object):

    def __init__(self, scan_id, state, queue_at, allocated_at, running_at, engine, properties):
        """

        Args:
            scan_id (str):
            state (str):
            queue_at (str):
            allocated_at (str):
            running_at (str):
            engine (str):
            properties (list of Property):
        """
        self.scan_id = scan_id
        self.state = state
        self.queue_at = queue_at
        self.allocated_at = allocated_at
        self.running_at = running_at
        self.engine = engine
        self.properties = properties

    def __str__(self):
        return """SastScan(scan_id={}, state={}, queue_at={}, allocated_at={}, running_at={}, engine={}, 
        properties={})""".format(
            self.scan_id, self.state, self.queue_at, self.allocated_at, self.running_at, self.engine,
            self.properties
        )
