from dataclasses import dataclass
from typing import List


@dataclass
class Composites:
    realm: List[str]
    client: dict
    application: dict
