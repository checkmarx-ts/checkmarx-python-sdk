from dataclasses import dataclass


@dataclass
class KeysMetadataRepresentationKeyMetadataRepresentation:
    algorithm: ... = None
    certificate: ... = None
    kid: ... = None
    provider_id: ... = None
    provider_priority: ... = None
    public_key: ... = None
    status: ... = None
    keys_metadata_representation_key_metadata_representation_type: ... = None
    use: ... = None

    @classmethod
    def from_dict(
        cls, item: dict
    ) -> "KeysMetadataRepresentationKeyMetadataRepresentation":
        return cls(
            algorithm=item.get("algorithm"),
            certificate=item.get("certificate"),
            kid=item.get("kid"),
            provider_id=item.get("providerId"),
            provider_priority=item.get("providerPriority"),
            public_key=item.get("publicKey"),
            status=item.get("status"),
            keys_metadata_representation_key_metadata_representation_type=item.get(
                "type"
            ),
            use=item.get("use"),
        )
