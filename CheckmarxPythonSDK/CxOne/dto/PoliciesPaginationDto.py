from dataclasses import dataclass, field
from typing import List, Optional

from .PolicyWebDto import PolicyWebDto


@dataclass
class PoliciesPaginationDto:
    """Paginated response from GET /policies/v2 and GET /policies/v3.

    Attributes:
        policies (List[PolicyWebDto]): Policies on the current page.
        filteredPoliciesCount (Optional[int]): Total count after filtering.
    """

    policies: List[PolicyWebDto] = field(default_factory=list)
    filteredPoliciesCount: Optional[int] = None

    @classmethod
    def from_dict(cls, item: dict) -> "PoliciesPaginationDto":
        return cls(
            policies=[
                PolicyWebDto.from_dict(p) for p in (item.get("policies") or [])
            ],
            filteredPoliciesCount=item.get("filteredPoliciesCount"),
        )
