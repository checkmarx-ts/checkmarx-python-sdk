class LogItem(object):

    def __init__(self, level, msg, time, error, worker, raw_log):
        """

        Args:
            level (str): error, warn, info, debug
            msg (str):
            time (str):
            error (str):
            worker (str):
            raw_log (str):
        """
        self.level = level
        self.msg = msg
        self.time = time
        self.error = error
        self.worker = worker
        self.raw_log = raw_log

    def __str__(self):
        return f"""LogItem(
        level={self.level},
        msg={self.msg},
        time={self.time},
        error={self.error},
        worker={self.worker},
        raw_log={self.raw_log},
        )"""

