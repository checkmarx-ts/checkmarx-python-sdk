class KeyStoreConfig:
    def __init__(self, key_store_config_format, key_alias, key_password, realm_alias, realm_certificate,
                 store_password):
        self.format = key_store_config_format
        self.keyAlias = key_alias
        self.keyPassword = key_password
        self.realmAlias = realm_alias
        self.realmCertificate = realm_certificate
        self.storePassword = store_password

    def __str__(self):
        return f"KeyStoreConfig(" \
               f"format={self.format} " \
               f"keyAlias={self.keyAlias} " \
               f"keyPassword={self.keyPassword} " \
               f"realmAlias={self.realmAlias} " \
               f"realmCertificate={self.realmCertificate} " \
               f"storePassword={self.storePassword} " \
               f")"

    def to_dict(self):
        return {
            "format": self.format,
            "keyAlias": self.keyAlias,
            "keyPassword": self.keyPassword,
            "realmAlias": self.realmAlias,
            "realmCertificate": self.realmCertificate,
            "storePassword": self.storePassword,
        }


def construct_key_store_config(item):
    return KeyStoreConfig(
        key_store_config_format=item.get("format"),
        key_alias=item.get("keyAlias"),
        key_password=item.get("keyPassword"),
        realm_alias=item.get("realmAlias"),
        realm_certificate=item.get("realmCertificate"),
        store_password=item.get("storePassword"),
    )
