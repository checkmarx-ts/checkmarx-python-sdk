class ClientProfileRepresentation:
    def __init__(self, description, executors, name):
        self.description = description
        self.executors = executors
        self.name = name

    def __str__(self):
        return f"ClientProfileRepresentation(" \
               f"description={self.description} " \
               f"executors={self.executors} " \
               f"name={self.name} " \
               f")"

    def to_dict(self):
        return {
            "description": self.description,
            "executors": self.executors,
            "name": self.name,
        }


def construct_client_profile_representation(item):
    return ClientProfileRepresentation(
        description=item.get("description"),
        executors=item.get("executors"),
        name=item.get("name"),
    )
