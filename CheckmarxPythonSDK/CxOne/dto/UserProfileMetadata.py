from dataclasses import dataclass
from typing import List
from .UserProfileAttributeMetadata import UserProfileAttributeMetadata
from .UserProfileAttributeGroupMetadata import UserProfileAttributeGroupMetadata


@dataclass
class UserProfileMetadata:
    attributes: List[UserProfileAttributeMetadata]
    groups: List[UserProfileAttributeGroupMetadata]
