class CertificateRepresentation:
    def __init__(self, certificate, kid, private_key, public_key):
        self.certificate = certificate
        self.kid = kid
        self.privateKey = private_key
        self.publicKey = public_key

    def __str__(self):
        return f"CertificateRepresentation(" \
               f"certificate={self.certificate} " \
               f"kid={self.kid} " \
               f"privateKey={self.privateKey} " \
               f"publicKey={self.publicKey} " \
               f")"

    def to_dict(self):
        return {
            "certificate": self.certificate,
            "kid": self.kid,
            "privateKey": self.privateKey,
            "publicKey": self.publicKey,
        }


def construct_certificate_representation(item):
    return CertificateRepresentation(
        certificate=item.get("certificate"),
        kid=item.get("kid"),
        private_key=item.get("privateKey"),
        public_key=item.get("publicKey"),
    )
