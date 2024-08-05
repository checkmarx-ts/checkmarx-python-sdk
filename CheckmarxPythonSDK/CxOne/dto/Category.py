class Category(object):

    def __init__(self, category_id, name, sast_id):
        """

        Args:
            category_id (int):
            name (str):
            sast_id (int):
        """
        self.category_id = category_id
        self.name = name
        self.sast_id = sast_id

    def __str__(self):
        return """Category(
        category_id={self.category_id},
        name={self.name},
        sast_id={self.sast_id},
        )"""
