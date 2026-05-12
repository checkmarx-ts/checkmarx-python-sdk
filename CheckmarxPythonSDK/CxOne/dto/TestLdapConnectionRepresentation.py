from dataclasses import dataclass


@dataclass
class TestLdapConnectionRepresentation:
    action: ... = None
    auth_type: ... = None
    bind_credential: ... = None
    bind_dn: ... = None
    component_id: ... = None
    connection_timeout: ... = None
    connection_url: ... = None
    start_tls: ... = None
    use_truststore_spi: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "TestLdapConnectionRepresentation":
        return cls(
            action=item.get("action"),
            auth_type=item.get("authType"),
            bind_credential=item.get("bindCredential"),
            bind_dn=item.get("bindDn"),
            component_id=item.get("componentId"),
            connection_timeout=item.get("connectionTimeout"),
            connection_url=item.get("connectionUrl"),
            start_tls=item.get("startTls"),
            use_truststore_spi=item.get("useTruststoreSpi"),
        )
