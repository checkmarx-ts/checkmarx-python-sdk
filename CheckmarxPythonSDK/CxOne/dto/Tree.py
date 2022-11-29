class Tree(object):
    def __init__(self, full_path, name, is_dir, files):
        """

        Args:
            full_path (str): path from the source project
            name (str): name of file or directory
            is_dir (bool): true if directory, otherwise false
            files (list of FileInfo):
        """
        self.FullPath = full_path
        self.name = name
        self.IsDir = is_dir
        self.Files = files

    def __str__(self):
        return """Tree(Files={}, name={}, IsDir={}, Files={})""".format(
            self.FullPath, self.name, self.IsDir, self.Files
        )
