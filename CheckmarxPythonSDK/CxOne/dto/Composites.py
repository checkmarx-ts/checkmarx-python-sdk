from dataclasses import dataclass
from typing import List


@dataclass
class Composites:
    realm: List[str]
    client: dict
    application: dict


def construct_composites(item):
    return Composites(
        realm=item.get("realm"),
        client=item.get("client"),
        application=item.get("application"),
    )
