class AddressClaimSet:
    def __init__(self, country, formatted, locality, postal_code, region, street_address):
        self.country = country
        self.formatted = formatted
        self.locality = locality
        self.postal_code = postal_code
        self.region = region
        self.street_address = street_address

    def __str__(self):
        return f"AddressClaimSet(" \
               f"country={self.country} " \
               f"formatted={self.formatted} " \
               f"locality={self.locality} " \
               f"postal_code={self.postal_code} " \
               f"region={self.region} " \
               f"street_address={self.street_address} " \
               f")"

    def to_dict(self):
        return {
            "country": self.country,
            "formatted": self.formatted,
            "locality": self.locality,
            "postal_code": self.postal_code,
            "region": self.region,
            "street_address": self.street_address,
        }


def construct_address_claim_set(item):
    return AddressClaimSet(
        country=item.get("country"),
        formatted=item.get("formatted"),
        locality=item.get("locality"),
        postal_code=item.get("postal_code"),
        region=item.get("region"),
        street_address=item.get("street_address"),
    )
