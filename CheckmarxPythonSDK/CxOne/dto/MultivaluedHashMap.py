from dataclasses import dataclass


@dataclass
class MultivaluedHashMap:
    empty: ... = None
    load_factor: ... = None
    threshold: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "MultivaluedHashMap":
        return cls(
            empty=item.get("empty"),
            load_factor=item.get("loadFactor"),
            threshold=item.get("threshold"),
        )
