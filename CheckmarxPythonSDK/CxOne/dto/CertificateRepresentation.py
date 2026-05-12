from dataclasses import dataclass


@dataclass
class CertificateRepresentation:
    certificate: ... = None
    kid: ... = None
    private_key: ... = None
    public_key: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "CertificateRepresentation":
        return cls(
            certificate=item.get("certificate"),
            kid=item.get("kid"),
            private_key=item.get("privateKey"),
            public_key=item.get("publicKey"),
        )
