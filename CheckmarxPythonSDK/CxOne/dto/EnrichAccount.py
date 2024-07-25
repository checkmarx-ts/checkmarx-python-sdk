class EnrichAccount(object):

    def __init__(self, name, account_id):
        """

        Args:
            name (str): The account name
            account_id (str): A unique identifier to the enrichment account
        """
        self.name = name
        self.account_id = account_id

    def __str__(self):
        return """EnrichAccount(name={}, account_id={})""".format(
            self.name, self.account_id
        )
