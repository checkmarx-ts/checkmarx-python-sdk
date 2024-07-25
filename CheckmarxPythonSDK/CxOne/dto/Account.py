class Account(object):

    def __init__(self, account_id, name, credentials, account_type, tenant_id, created_at, updated_at, last_scan_date):
        """

        Args:
            account_id (str): A unique identifier for an account
            name (str): The account name
            credentials (dict): The account credentials to connect to the provider
            account_type (int): The type of account
            tenant_id (str): The tenantId where the account belongs to
            created_at (str):
            updated_at (str):
            last_scan_date (str):
        """
        self.account_id = account_id
        self.name = name
        self.credentials = credentials
        self.account_type = account_type
        self.tenant_id = tenant_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_scan_date = last_scan_date

    def __str__(self):
        return """Account(account_id={}, name={}, credentials={}, account_type={}, tenant_id={}, created_at={}, 
        updated_at={}, last_scan_date={})""".format(
            self.account_id, self.name, self.credentials, self.account_type, self.tenant_id, self.created_at,
            self.updated_at, self.last_scan_date
        )
