from dataclasses import dataclass


@dataclass
class FileInfo:
    name: str = None
    mod_time: str = None
    size: str = None
    is_dir: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "FileInfo":
        return cls(
            name=item.get("name"),
            mod_time=item.get("modTime"),
            size=item.get("size"),
            is_dir=item.get("isDir"),
        )
