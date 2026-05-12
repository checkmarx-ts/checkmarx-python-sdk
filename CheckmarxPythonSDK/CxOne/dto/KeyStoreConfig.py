from dataclasses import dataclass


@dataclass
class KeyStoreConfig:
    key_store_config_format: ... = None
    key_alias: ... = None
    key_password: ... = None
    realm_alias: ... = None
    realm_certificate: ... = None
    store_password: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "KeyStoreConfig":
        return cls(
            key_store_config_format=item.get("format"),
            key_alias=item.get("keyAlias"),
            key_password=item.get("keyPassword"),
            realm_alias=item.get("realmAlias"),
            realm_certificate=item.get("realmCertificate"),
            store_password=item.get("storePassword"),
        )
