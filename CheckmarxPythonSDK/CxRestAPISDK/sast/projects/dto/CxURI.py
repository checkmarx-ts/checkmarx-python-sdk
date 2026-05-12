# encoding: utf-8


class CxURI(object):
    """
    the URI settings
    """

    def __init__(self, absolute_url, port):
        self.absolute_url = absolute_url
        self.port = port

    @classmethod
    def from_dict(cls, item: dict) -> "CxURI":
        return cls(
            absolute_url=item.get("absoluteUrl"),
            port=item.get("port"),
        )

    def __str__(self):
        return "CxURI(absolute_url={}, port={})".format(self.absolute_url, self.port)
