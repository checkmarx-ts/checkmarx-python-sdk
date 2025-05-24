class CommentJSON(object):
    def __init__(self, id: str = None, date: str = None, user: str = None, content: str = None,
                 is_deleted: bool = None):
        self.id = id
        self.date = date
        self.user = user
        self.content = content
        self.isDeleted = is_deleted

    def __str__(self):
        return (f"CommentJSON(id={self.id}, date={self.date}, user={self.user}, content={self.content},"
                f" isDeleted={self.isDeleted})")
