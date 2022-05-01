class FileInfo(object):
    def __init__(self, name, mod_time, size, is_dir):
        """

        Args:
            name (str): Name of the file or directory.
            mod_time (str): The time that the file or directory was last modified.
            size (int): The size of the file or directory.
            is_dir (bool): Indicates whether the entry in this directory a file or a directory.
        """
        self.name = name
        self.modTime = mod_time
        self.size = size
        self.isDir = is_dir

    def __str__(self):
        return """FileInfo(name={}, modTime={}, size={}, isDir={})""".format(
            self.name, self.modTime, self.size, self.isDir
        )
