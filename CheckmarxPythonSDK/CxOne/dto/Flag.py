from dataclasses import dataclass


@dataclass
class Flag:
    name: str = None
    status: bool = None
    payload: dict = None

    def __eq__(self, other):

        return (self.name == other.name and
                self.status == other.status and
                self.payload == other.payload)

    def __lt__(self, other):

        return self.name < other.name


def construct_feature_flag(item):
    return Flag(
        name=item.get("name"),
        status=item.get("status"),
        payload=item.get("payload")
    )
