# encoding: utf-8


class ServiceProvider(object):

    def __init__(self, service_provider_id, name):
        """

        Args:
            service_provider_id (int):
            name (str):
        """
        self.id = service_provider_id
        self.name = name

    def __str__(self):
        return """ServiceProvider(id={}, name={})""".format(self.id, self.name)
