class ScanInfo(object):

    def __init__(self, scan_id, project_id, loc, file_count, is_incremental, is_incremental_canceled,
                 incremental_cancel_reason, based_id, added_files_count, changed_files_count, deleted_files_count,
                 change_percentage, query_preset):
        """

        Args:
            scan_id (str):
            project_id (str):
            loc (int):
            file_count (int):
            is_incremental (bool):
            is_incremental_canceled (bool):
            incremental_cancel_reason (str):
            based_id (str):
            added_files_count (int):
            changed_files_count (int):
            deleted_files_count (int):
            change_percentage (float):
            query_preset (str):
        """
        self.scan_id = scan_id
        self.project_id = project_id
        self.loc = loc
        self.file_count = file_count
        self.is_incremental = is_incremental
        self.is_incremental_canceled = is_incremental_canceled
        self.incremental_cancel_reason = incremental_cancel_reason
        self.based_id = based_id
        self.added_files_count = added_files_count
        self.changed_files_count = changed_files_count
        self.deleted_files_count = deleted_files_count
        self.change_percentage = change_percentage
        self.query_preset = query_preset

    def __str__(self):
        return f"""
        ScanInfo(
        scan_id={self.scan_id}, 
        project_id={self.project_id}, 
        loc={self.loc}, 
        file_count={self.file_count}, 
        is_incremental={self.is_incremental}, 
        is_incremental_canceled={self.is_incremental_canceled}, 
        incremental_cancel_reason={self.incremental_cancel_reason}, 
        based_id={self.based_id}, 
        added_files_count={self.added_files_count}, 
        changed_files_count={self.changed_files_count}, 
        deleted_files_count={self.deleted_files_count}, 
        change_percentage={self.change_percentage}, 
        query_preset={self.query_preset}
        )
        """
