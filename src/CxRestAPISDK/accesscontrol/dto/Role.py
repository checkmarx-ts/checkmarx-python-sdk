# encoding: utf-8


class Role(object):

    def __init__(self, role_id, is_system_role, name, description, permission_ids):
        """

        Args:
            role_id (int):
            is_system_role (boolean):
            name (str):
            description (str):
            permission_ids (list of int):
        """
        self.id = role_id
        self.is_system_role = is_system_role
        self.name = name
        self.description = description
        self.permission_ids = permission_ids

    def __str__(self):
        return """Role(id={}, is_system_role={}, name={}, description={}, permission_ids={})""".format(
            self.id, self.is_system_role, self.name, self.description, self.permission_ids
        )
