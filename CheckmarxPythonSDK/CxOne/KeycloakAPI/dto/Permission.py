class Permission:
    def __init__(self, claims, rsid, rsname, scopes):
        self.claims = claims
        self.rsid = rsid
        self.rsname = rsname
        self.scopes = scopes

    def __str__(self):
        return f"Permission(" \
               f"claims={self.claims} " \
               f"rsid={self.rsid} " \
               f"rsname={self.rsname} " \
               f"scopes={self.scopes} " \
               f")"

    def to_dict(self):
        return {
            "claims": self.claims,
            "rsid": self.rsid,
            "rsname": self.rsname,
            "scopes": self.scopes,
        }


def construct_permission(item):
    return Permission(
        claims=item.get("claims"),
        rsid=item.get("rsid"),
        rsname=item.get("rsname"),
        scopes=item.get("scopes"),
    )
