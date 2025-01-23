class ClientInitialAccessPresentation:
    def __init__(self, count, expiration, client_initial_access_presentation_id, remaining_count, timestamp, token):
        self.count = count
        self.expiration = expiration
        self.id = client_initial_access_presentation_id
        self.remainingCount = remaining_count
        self.timestamp = timestamp
        self.token = token

    def __str__(self):
        return f"ClientInitialAccessPresentation(" \
               f"count={self.count} " \
               f"expiration={self.expiration} " \
               f"id={self.id} " \
               f"remainingCount={self.remainingCount} " \
               f"timestamp={self.timestamp} " \
               f"token={self.token} " \
               f")"

    def to_dict(self):
        return {
            "count": self.count,
            "expiration": self.expiration,
            "id": self.id,
            "remainingCount": self.remainingCount,
            "timestamp": self.timestamp,
            "token": self.token,
        }


def construct_client_initial_access_presentation(item):
    return ClientInitialAccessPresentation(
        count=item.get("count"),
        expiration=item.get("expiration"),
        client_initial_access_presentation_id=item.get("id"),
        remaining_count=item.get("remainingCount"),
        timestamp=item.get("timestamp"),
        token=item.get("token"),
    )
