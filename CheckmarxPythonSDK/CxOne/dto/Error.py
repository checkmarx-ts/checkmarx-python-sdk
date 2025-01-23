class Error:
    def __init__(self, message, error_type, code):
        self.message = message
        self.type = error_type
        self.code = code

    def __str__(self):
        return f"Error(" \
               f"message={self.message} " \
               f"type={self.type} " \
               f"code={self.code} " \
               f")"

    def to_dict(self):
        return {
            "message": self.message,
            "type": self.type,
            "code": self.code,
        }


def construct_error(item):
    return Error(
        message=item.get("message"),
        error_type=item.get("type"),
        code=item.get("code"),
    )
