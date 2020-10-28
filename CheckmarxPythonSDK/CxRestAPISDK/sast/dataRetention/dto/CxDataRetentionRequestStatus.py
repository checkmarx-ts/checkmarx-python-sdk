# encoding: utf-8


class CxDataRetentionRequestStatus(object):
    """
    data retention request status
    """

    def __init__(self, status_id, stage, link):
        """

        Args:
            status_id (int):
            stage (:obj:`CxDataRetentionRequestStatusStage`:
            link (:obj:`CxLink`):
        """
        self.id = status_id
        self.stage = stage
        self.link = link

    def __str__(self):
        return "CxDataRetentionRequestStatus(id={}, stage={}, link={})".format(
            self.id, self.stage, self.link
        )
