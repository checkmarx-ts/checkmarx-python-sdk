from dataclasses import dataclass
from .Metadata import Metadata, construct_metadata


@dataclass
class QueryRequest:
    path: str = None
    name: str = None
    source: str = None
    metadata: Metadata = None

    def to_dict(self):
        return {
          "path": self.path,
          "name": self.name,
          "source": self.source,
          "metadata": construct_metadata(self.metadata)
        }

