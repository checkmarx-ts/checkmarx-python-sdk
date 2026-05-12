from dataclasses import dataclass
from typing import Optional


@dataclass
class SAMLServiceProvider:
    assertion_consumer_service_url: Optional[str] = None
    certificate_file_name: Optional[str] = None
    certificate_subject: Optional[str] = None
    issuer: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SAMLServiceProvider":
        return cls(
            assertion_consumer_service_url=item.get("assertionConsumerServiceUrl"),
            certificate_file_name=item.get("certificateFileName"),
            certificate_subject=item.get("certificateSubject"),
            issuer=item.get("issuer"),
        )
