from dataclasses import dataclass


@dataclass
class VersionsOut:
    """
    Attributes:
        sast (str): sast engine version
        kics (str): IaC Security (KICS) engine version
        cx_one (str): CxOne version
    """
    sast: str
    kics: str
    cx_one: str


def construct_versions_out(item):
    return VersionsOut(
        sast=item.get("SAST"),
        kics=item.get("KICS"),
        cx_one=item.get("CxOne")
    )
