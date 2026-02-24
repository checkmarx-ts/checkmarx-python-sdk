from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class KeyUse:
    value: str

    def to_dict(self) -> str:
        return self.value

    @classmethod
    def from_dict(cls, data: Union[str, Dict[str, Any]]) -> Self:
        if isinstance(data, str):
            return cls(value=data)
        elif isinstance(data, dict):
            snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}
            return cls(**snake_data)
        else:
            raise ValueError(f'Invalid data type for KeyUse: {type(data)}')
