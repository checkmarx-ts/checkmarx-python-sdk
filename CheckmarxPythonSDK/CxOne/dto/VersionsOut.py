from dataclasses import dataclass


@dataclass
class VersionsOut:
    """
    Attributes:
        sast (str): sast engine version
        kics (str): IaC Security (KICS) engine version
        cx_one (str): CxOne version
    """

    sast: str = None
    kics: str = None
    cx_one: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "VersionsOut":
        return cls(
            sast=item.get("SAST"),
            kics=item.get("KICS"),
            cx_one=item.get("CxOne"),
        )
