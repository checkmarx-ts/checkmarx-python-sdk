# encoding: utf-8


class Permission(object):

    def __init__(self, permission_id, service_provider_id, name, category):
        """

        Args:
            permission_id (int):
            service_provider_id (int):
            name (str):
            category (str):
        """
        self.id = permission_id
        self.service_provider_id = service_provider_id
        self.name = name
        self.category = category

    def __str__(self):
        return """Permission(id={}, service_provider_id={}, name={}, category={})""".format(
            self.id, self.service_provider_id, self.name, self.category
        )
