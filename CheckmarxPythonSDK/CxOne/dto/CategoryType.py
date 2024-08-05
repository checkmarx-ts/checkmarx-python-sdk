class CategoryType(object):

    def __init__(self, category_type_id, name, sast_id, order, categories):
        """

        Args:
            category_type_id (int):
            name (str):
            sast_id (int):
            order (int):
            categories (list of Category):
        """
        self.category_type_id = category_type_id
        self.name = name
        self.sast_id = sast_id
        self.order = order
        self.categories = categories

    def __str__(self):
        return """CategoryType(
        category_type_id={self.category_type_id},
        name={self.name},
        sast_id={self.sast_id},
        order={self.order},
        categories={self.categories},
        )"""
