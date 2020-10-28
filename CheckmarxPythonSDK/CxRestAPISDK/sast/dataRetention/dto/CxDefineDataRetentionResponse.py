# encoding: utf-8


class CxDefineDataRetentionResponse(object):
    """
    define data retention response
    """
    def __init__(self, data_retention_response_id, link):
        """

        Args:
            data_retention_response_id (int):
            link (:obj:`CxLink`):
        """
        self.id = data_retention_response_id
        self.link = link

    def __str__(self):
        return "CxDefineDataRetentionResponse(id={}, link={})".format(
            self.id, self.link
        )
