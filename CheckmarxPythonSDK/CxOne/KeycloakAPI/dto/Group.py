class Group:

    def __init__(self, group_id, name, path, sub_groups):
        """

        Args:
            group_id (str):
            name (str):
            path (str):
            sub_groups (list of Group):
        """
        self.id = group_id
        self.name = name
        self.path = path
        self.subGroups = sub_groups

    def __str__(self):
        return f"Group(" \
               f"id={self.id} " \
               f"name={self.name} " \
               f"path={self.path} " \
               f"subGroups={self.subGroups}" \
               f")"


def construct_group(item):
    return Group(
        group_id=item.get("id"),
        name=item.get("name"),
        path=item.get("path"),
        sub_groups=[construct_group(group) for group in item.get("subGroups") or []]
    )
