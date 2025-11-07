class MultivaluedHashMap:
    def __init__(self, empty, load_factor, threshold):
        self.empty = empty
        self.loadFactor = load_factor
        self.threshold = threshold

    def __str__(self):
        return f"MultivaluedHashMap(" \
               f"empty={self.empty} " \
               f"loadFactor={self.loadFactor} " \
               f"threshold={self.threshold} " \
               f")"

    def to_dict(self):
        return {
            "empty": self.empty,
            "loadFactor": self.loadFactor,
            "threshold": self.threshold,
        }


def construct_multivalued_hash_map(item):
    return MultivaluedHashMap(
        empty=item.get("empty"),
        load_factor=item.get("loadFactor"),
        threshold=item.get("threshold"),
    )
