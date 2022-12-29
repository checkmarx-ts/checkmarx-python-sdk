class Line:
    def __init__(self, number, code):
        """

        Args:
            number (int): line number
            code (str): source code snippet
        """
        self.Number = number
        self.Code = code

    def __str__(self):
        return """Line(number={}, code={})""".format(self.Number, self.Code)


def construct_line(number, code):
    return Line(
        number=int(number),
        code=code
    )
