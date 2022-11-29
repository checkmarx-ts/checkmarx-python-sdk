class MethodInfo(object):
    def __init__(self, lang, name, member_of, documentation, return_type, kind, parameters):
        """

        Args:
            lang (str):
            name (str):
            member_of (str):
            documentation (str):
            return_type (str):
            kind (str):
            parameters (list of MethodParameter):
        """
        self.lang = lang
        self.name = name
        self.memberOf = member_of
        self.documentation = documentation
        self.returnType = return_type
        self.kind = kind
        self.parameters = parameters

    def __str__(self):
        return """MethodInfo(lang={}, name={}, memberOf={}, documentation={}, returnType={}, 
        kind={}, parameters={})""".format(
            self.lang, self.name, self.memberOf, self.documentation, self.returnType, self.kind, self.parameters
        )
