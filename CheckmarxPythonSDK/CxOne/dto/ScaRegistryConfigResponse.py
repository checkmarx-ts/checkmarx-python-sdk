from dataclasses import dataclass


@dataclass
class ScaRegistryConfigResponse:
    """Response from creating a private registry configuration.

    Attributes:
        id (str): Unique identifier of the created configuration.
        message (str): Human-readable text describing the result.
    """

    id: str = None
    message: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScaRegistryConfigResponse":
        return cls(
            id=item.get("id"),
            message=item.get("message"),
        )
