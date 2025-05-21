class Queries(object):
    def __init__(self, id: int = None, name: str = None, group: str = None, level: str = None, lang: str = None,
                 modify: str = None, is_executable: bool = None):
        self.id = id
        self.name = name
        self.group = group
        self.level = level
        self.lang = lang
        self.modify = modify
        self.isExecutable = is_executable

    def __str__(self):
        return f"""Queries(
        id={self.id}, 
        name={self.name}, 
        group={self.group}, 
        level={self.level}, 
        lang={self.lang}, 
        modify={self.modify}, 
        isExecutable={self.isExecutable}
        )"""
