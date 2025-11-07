class TestLdapConnectionRepresentation:
    def __init__(self, action, auth_type, bind_credential, bind_dn, component_id, connection_timeout, connection_url,
                 start_tls, use_truststore_spi):
        self.action = action
        self.authType = auth_type
        self.bindCredential = bind_credential
        self.bindDn = bind_dn
        self.componentId = component_id
        self.connectionTimeout = connection_timeout
        self.connectionUrl = connection_url
        self.startTls = start_tls
        self.useTruststoreSpi = use_truststore_spi

    def __str__(self):
        return f"TestLdapConnectionRepresentation(" \
               f"action={self.action}, " \
               f"authType={self.authType}, " \
               f"bindCredential={self.bindCredential}, " \
               f"bindDn={self.bindDn}, " \
               f"componentId={self.componentId}, " \
               f"connectionTimeout={self.connectionTimeout}, " \
               f"connectionUrl={self.connectionUrl}, " \
               f"startTls={self.startTls}, " \
               f"useTruststoreSpi={self.useTruststoreSpi}" \
               f")"

    def to_dict(self):
        return {
            "action": self.action,
            "authType": self.authType,
            "bindCredential": self.bindCredential,
            "bindDn": self.bindDn,
            "componentId": self.componentId,
            "connectionTimeout": self.connectionTimeout,
            "connectionUrl": self.connectionUrl,
            "startTls": self.startTls,
            "useTruststoreSpi": self.useTruststoreSpi,
        }


def construct_test_ldap_connection_representation(item):
    return TestLdapConnectionRepresentation(
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
