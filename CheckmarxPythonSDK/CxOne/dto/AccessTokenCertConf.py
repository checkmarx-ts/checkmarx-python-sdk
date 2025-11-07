class AccessTokenCertConf:
    def __init__(self, x5t):
        self.x5t = x5t

    def __str__(self):
        return f"AccessTokenCertConf(" \
               f"x5t#S256={self.x5t} " \
               f")"


def to_dict(self):
    return {
        "x5t#S256": self.x5t
    }


def construct_access_token_cert_conf(item):
    return AccessTokenCertConf(
        x5t=item.get("x5t"),
    )
