from dataclasses import dataclass
from typing import Optional


@dataclass
class PackageRiskItem:
    """One package version to look up in a PackageRisksRequest.

    When `format` is "Package": `type`, `name`, and `version` are
    required (`name` must have reserved characters URL-encoded, e.g.
    "/" -> "%2F"). When `format` is "Purl": `purl` is required instead.
    """
    type: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    purl: Optional[str] = None
