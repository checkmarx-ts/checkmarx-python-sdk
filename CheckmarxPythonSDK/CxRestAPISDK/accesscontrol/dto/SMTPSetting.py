# encoding: utf-8


class SMTPSetting(object):

    def __init__(self, smtp_settings_id, host, port, encryption_type, from_address, use_default_credentials, username):
        """

        Args:
            smtp_settings_id (int):
            host (str):
            port (int):
            encryption_type (str):
            from_address: (str)
            use_default_credentials (bool):
            username (str):
        """

        self.id = smtp_settings_id
        self.host = host
        self.port = port
        self.encryption_type = encryption_type
        self.from_address = from_address
        self.use_default_credentials = use_default_credentials
        self.username = username

    def __str__(self):
        return """SMTPSetting(id={}, host={}, port={}, encryption_type={}, from_address={], use_default_credentials={}, 
        username={})""".format(self.id, self.host, self.port, self.encryption_type, self.from_address,
                               self.use_default_credentials, self.username)
