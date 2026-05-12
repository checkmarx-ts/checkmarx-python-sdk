from dataclasses import dataclass


@dataclass
class AddressClaimSet:
    country: ... = None
    formatted: ... = None
    locality: ... = None
    postal_code: ... = None
    region: ... = None
    street_address: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AddressClaimSet":
        return cls(
            country=item.get("country"),
            formatted=item.get("formatted"),
            locality=item.get("locality"),
            postal_code=item.get("postal_code"),
            region=item.get("region"),
            street_address=item.get("street_address"),
        )
