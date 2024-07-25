class Container(object):

    def __init__(self, container_id, cluster_name, container_name, public_exposed, image, image_short_name, project):
        """

        Args:
            container_id (str):
            cluster_name (str):
            container_name (str):
            public_exposed (str):
            image (str):
            image_short_name (str):
            project (str):
        """
        self.container_id = container_id
        self.cluster_name = cluster_name
        self.container_name = container_name
        self.public_exposed = public_exposed
        self.image = image
        self.image_short_name = image_short_name
        self.project = project

    def __str__(self):
        return """Container(container_id={}, cluster_name={}, container_name={}, public_exposed={}, image={},
         image_short_name={}, project={})""".format(
            self.container_id, self.cluster_name, self.container_name, self.public_exposed, self.image,
            self.image_short_name, self.project
        )
