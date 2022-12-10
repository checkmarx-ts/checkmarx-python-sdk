class ClientInitialAccessCreatePresentation:
    def __init__(self, count, expiration):
        self.count = count
        self.expiration = expiration

    def __str__(self):
        return f"ClientInitialAccessCreatePresentation(" \
               f"count={self.count} " \
               f"expiration={self.expiration} " \
               f")"

    def get_post_data(self):
        import json
        return json.dumps({
            "count": self.count,
            "expiration": self.expiration,
        })


def construct_client_initial_access_create_presentation(item):
    return ClientInitialAccessCreatePresentation(
        count=item.get("count"),
        expiration=item.get("expiration"),
    )
