
class User(object):

    def __init__(self, user_id, user_name, first_name, last_name, email):
        """

        Args:
            user_id (int):
            user_name (str):
            first_name (str):
            last_name (str):
            email (str):
        """
        self.id = user_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return """User(user_id={}, user_name={}, first_name={}, last_name={}, email={})""".format(
            self.id, self.user_name, self.first_name, self.last_name, self.email
        )
