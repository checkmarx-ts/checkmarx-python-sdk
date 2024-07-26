class EngineData(object):

    def __init__(self, engine, risk_level, last_scan_id, severity_counters):
        """

        Args:
            engine (str): The name of the scanning engine.
            risk_level (str): The risk level reported by the engine.
            last_scan_id (str): The ID of the last scan performed by the engine.
            severity_counters (list of SeverityCounter):
        """
        self.engine = engine
        self.risk_level = risk_level
        self.last_scan_id = last_scan_id
        self.severity_counters = severity_counters

    def __str__(self):
        return """EngineData(engine={}, risk_level={}, last_scan_id={}, severity_counters={})""".format(
            self.engine, self.risk_level, self.last_scan_id, self.severity_counters
        )
