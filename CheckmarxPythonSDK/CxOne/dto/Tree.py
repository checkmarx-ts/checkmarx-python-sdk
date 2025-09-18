from dataclasses import dataclass
from typing import List
from .FileInfo import FileInfo, construct_file_info


@dataclass
class Tree:
    """

    Args:
        full_path (str): path from the source project
        name (str): name of file or directory
        is_dir (bool): true if directory, otherwise false
        files (list of FileInfo):
    """
    full_path: str
    name: str
    is_dir: bool
    files: List[FileInfo]


def construct_tree(item):
    return Tree(
        full_path=item.get("FullPath"),
        name=item.get("name"),
        is_dir=item.get("IsDir"),
        files=[
            construct_file_info(file) for file in item.get("Files", [])
        ]
    )
