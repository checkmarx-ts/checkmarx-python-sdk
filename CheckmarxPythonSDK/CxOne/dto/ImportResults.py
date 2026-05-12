from dataclasses import dataclass


@dataclass
class ImportResults:
    """
    Args:
        import_id (str): The id of the new import
    """

    import_id: str

    @classmethod
    def from_dict(cls, item: dict) -> "ImportResults":
        return cls(import_id=item.get("importId"))
