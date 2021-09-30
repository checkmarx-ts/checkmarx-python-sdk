class CxProjectQueueSetting(object):

    def __init__(self, queue_keep_mode=None, scans_type=None, include_scans_in_process=None,
                 identical_code_only=None):
        """

        Args:
            queue_keep_mode (str):
            scans_type (str):
            include_scans_in_process (bool):
            identical_code_only (bool):
        """
        self.queue_keep_mode = queue_keep_mode
        self.scans_type = scans_type
        self.include_scans_in_process = include_scans_in_process
        self.identical_code_only = identical_code_only

    def __str__(self):
        return """CxProjectQueueSetting(queue_keep_mode={}, scans_type={}, include_scans_in_process={},
                 identical_code_only={})""".format(
            self.queue_keep_mode, self.scans_type, self.include_scans_in_process, self.identical_code_only
        )
