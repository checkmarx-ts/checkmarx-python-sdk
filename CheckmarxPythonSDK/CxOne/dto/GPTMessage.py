
class GPTMessage:
    def __init__(self, role: str = None, content: str = None):
        self.role = role
        self.content = content

    def __str__(self):
        return f"GPTMessage(role={self.role}, content={self.content})"
