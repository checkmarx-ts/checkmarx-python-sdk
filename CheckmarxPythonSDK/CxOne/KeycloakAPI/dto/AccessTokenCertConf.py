class AccessTokenCertConf:
    def __init__(self, x5t#_s256):
        self.x5t#S256 = x5t#_s256

    def __str__(self):
        return f"AccessTokenCertConf(" \
               f"x5t#S256={self.x5t#S256}" \
               f")"

    def get_post_data(self):
        import json
        return json.dumps({
            "x5t#S256": self.x5t#S256,
        })

def construct_access_token_cert_conf(item):
    return AccessTokenCertConf(
        x5t#_s256=item.get("x5t#S256"),
    )
