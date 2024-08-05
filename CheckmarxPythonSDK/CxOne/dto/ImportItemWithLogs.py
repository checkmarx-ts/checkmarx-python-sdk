class ImportItemWithLogs(object):

    def __init__(self, migration_id, status, created_at, logs):
        """

        Args:
            migration_id (str):
            status (str): pending, running, completed, failed
            created_at (str):
            logs (list of LogItem):
        """
        self.migration_id = migration_id
        self.status = status
        self.created_at = created_at
        self.logs = logs

    def __str__(self):
        return f"""ImportItemWithLogs(
        migration_id={self.migration_id},
        status={self.status},
        created_at={self.created_at},
        logs={self.logs},
        )"""
