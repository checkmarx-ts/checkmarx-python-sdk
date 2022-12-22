class AstIdWithName:
    def __init__(self, group_id, group_name):
        """

        Args:
            group_id (str):
            group_name (str):
        """
        self.id = group_id
        self.name = group_name

    def __str__(self):
        return f"AstIdWithName("\
               f"id={self.id}, " \
               f"name={self.name}" \
               f")"


def construct_ast_id_with_name(item):
    return AstIdWithName(
        group_id=item.get("id"),
        group_name=item.get("name")
    )
