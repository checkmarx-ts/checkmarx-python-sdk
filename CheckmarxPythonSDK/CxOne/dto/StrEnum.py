from enum import Enum
from typing import Any


class StrEnum(str, Enum):

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: '{self.value}'>"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def get(cls, value: str) -> Any:
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' is not valid {cls.__name__}")

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def names(cls):
        return [member.name for member in cls]

    @classmethod
    def has_value(cls, value: str) -> bool:
        """检查值是否存在"""
        return any(member.value == value for member in cls)