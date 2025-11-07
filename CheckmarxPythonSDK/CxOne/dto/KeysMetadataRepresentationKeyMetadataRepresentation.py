class KeysMetadataRepresentationKeyMetadataRepresentation:
    def __init__(self, algorithm, certificate, kid, provider_id, provider_priority, public_key, status,
                 keys_metadata_representation_key_metadata_representation_type, use):
        self.algorithm = algorithm
        self.certificate = certificate
        self.kid = kid
        self.providerId = provider_id
        self.providerPriority = provider_priority
        self.publicKey = public_key
        self.status = status
        self.type = keys_metadata_representation_key_metadata_representation_type
        self.use = use

    def __str__(self):
        return f"KeysMetadataRepresentationKeyMetadataRepresentation(" \
               f"algorithm={self.algorithm} " \
               f"certificate={self.certificate} " \
               f"kid={self.kid} " \
               f"providerId={self.providerId} " \
               f"providerPriority={self.providerPriority} " \
               f"publicKey={self.publicKey} " \
               f"status={self.status} " \
               f"type={self.type} " \
               f"use={self.use} " \
               f")"

    def to_dict(self):
        return {
            "algorithm": self.algorithm,
            "certificate": self.certificate,
            "kid": self.kid,
            "providerId": self.providerId,
            "providerPriority": self.providerPriority,
            "publicKey": self.publicKey,
            "status": self.status,
            "type": self.type,
            "use": self.use,
        }


def construct_keys_metadata_representation_key_metadata_representation(item):
    return KeysMetadataRepresentationKeyMetadataRepresentation(
        algorithm=item.get("algorithm"),
        certificate=item.get("certificate"),
        kid=item.get("kid"),
        provider_id=item.get("providerId"),
        provider_priority=item.get("providerPriority"),
        public_key=item.get("publicKey"),
        status=item.get("status"),
        keys_metadata_representation_key_metadata_representation_type=item.get("type"),
        use=item.get("use"),
    )
