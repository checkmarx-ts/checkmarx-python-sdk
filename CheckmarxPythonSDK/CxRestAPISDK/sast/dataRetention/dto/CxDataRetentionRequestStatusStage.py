# encoding: utf-8


class CxDataRetentionRequestStatusStage(object):
    """
    data retention request status stage
    """
    def __init__(self, stage_id, value):
        """

        Args:
            stage_id (int):
            value (str):
        """
        self.id = stage_id
        self.value = value

    def __str__(self):
        return "CxDataRetentionRequestStatusStage(id={}, value={})".format(
            self.id, self.value
        )
