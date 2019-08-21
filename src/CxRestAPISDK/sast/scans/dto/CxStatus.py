# encoding: utf-8


class CxStatus(object):
    """
    scan status
    """

    class Detail(object):
        """
        scan status detail
        """

        def __init__(self, stage, step):
            """

            :param stage: str
            :param step: str
            """
            self.stage = stage
            self.step = step

    def __init__(self, id=None, name=None, details=None):
        """

        :param id: int
        :param name: str
        :param details: CxStatus.Detail
        """
        self.id = id
        self.name = name
        self.details = details
