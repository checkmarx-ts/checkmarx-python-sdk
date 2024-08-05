class ImportItem(object):

    def __init__(self, migration_id, status, created_at):
        """

        Args:
            migration_id (str):
            status (str): pending, running, completed, failed
            created_at (str):
        """
        self.migration_id = migration_id
        self.status = status
        self.created_at = created_at

    def __str__(self):
        return f"""ImportItem(
        migration_id={self.migration_id},
        status={self.status},
        created_at={self.created_at},
        )"""
