from .Metadata import Metadata


class QueryRequest(object):
    def __init__(self, path: str = None, name: str = None, source: str = None, metadata: Metadata = None):
        self.path = path
        self.name = name
        self.source = source
        self.metadata = metadata

    def __str__(self):
        return f"QueryRequest(path={self.path}, name={self.name}, source={self.source}, metadata={self.metadata})"

    def to_dict(self):
        return {
          "path": self.path,
          "name": self.name,
          "source": self.source,
          "metadata": self.metadata
        }

