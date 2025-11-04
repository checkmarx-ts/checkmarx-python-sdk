from enum import Enum, auto
import inspect


class StrEnum(str, Enum):

    @staticmethod
    def _auto_():
        frame = inspect.currentframe().f_back.f_back
        member_name = frame.f_code.co_name
        return member_name

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
