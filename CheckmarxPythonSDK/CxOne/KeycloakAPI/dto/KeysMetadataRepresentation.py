class KeysMetadataRepresentation:
    def __init__(self, active, keys):
        self.active = active
        self.keys = keys

    def __str__(self):
        return f"KeysMetadataRepresentation(" \
               f"active={self.active} " \
               f"keys={self.keys} " \
               f")"

    def get_post_data(self):
        import json
        return json.dumps({
            "active": self.active,
            "keys": self.keys,
        })


def construct_keys_metadata_representation(item):
    return KeysMetadataRepresentation(
        active=item.get("active"),
        keys=item.get("keys"),
    )
