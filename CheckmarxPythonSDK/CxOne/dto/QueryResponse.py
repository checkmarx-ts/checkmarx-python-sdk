from .Metadata import Metadata


class QueryResponse(object):
    def __init__(self, id: str = None, name: str = None, level: str = None, path: str = None, source: str = None,
                 metadata: Metadata = None):
        self.id = id
        self.name = name
        self.level = level
        self.path = path
        self.source = source
        self.metadata = metadata

    def __str__(self):
        return (f"QueryResponse(id={self.id}, name={self.name}, level={self.level}, "
                f"path={self.path}, source={self.source}, "
                f"metadata={self.metadata})")
