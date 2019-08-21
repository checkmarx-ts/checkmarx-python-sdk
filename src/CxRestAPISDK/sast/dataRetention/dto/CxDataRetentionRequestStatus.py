# encoding: utf-8


class CxDataRetentionRequestStatus(object):
    """
    data retention request status
    """
    class Stage(object):
        def __init__(self, id, value):
            """

            :param id: int
            :param value: str
            """
            self.id = id
            self.value = value

    def __init__(self, id, stage, link):
        """

        :param id: int
        :param stage: CxDataRetentionRequestStatus.Stage
        :param link: CxLink
        """
        self.id = id
        self.stage = stage
        self.link = link
