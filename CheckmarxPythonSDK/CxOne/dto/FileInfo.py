from dataclasses import dataclass


@dataclass
class FileInfo:
    name: str = None  # Name of the file or directory.
    mod_time: str = None  # The time that the file or directory was last modified.
    size: str = None  # The size of the file or directory.
    is_dir: str = None  # Indicates whether the entry in this directory a file or a directory.


def construct_file_info(item):
    return FileInfo(
        name=item.get("name"),
        mod_time=item.get("modTime"),
        size=item.get("size"),
        is_dir=item.get("isDir"),
    )
