# encoding: utf-8


class User(object):

    def __init__(self, user_id=None, username=None, last_login_date=None, role_ids=None, team_ids=None,
                 authentication_provider_id=None, first_name=None, last_name=None, email=None, phone_number=None,
                 cell_phone_number=None, job_title=None, other=None, country=None, active=None, expiration_date=None,
                 allowed_ip_list=None, locale_id=None):
        """

        Args:
            user_id (int):
            username (str):
            last_login_date (str):
            role_ids (list[int]):
            team_ids (list[int]):
            authentication_provider_id (int):
            first_name (str):
            last_name (str):
            email (str):
            phone_number (str):
            cell_phone_number (str):
            job_title (str):
            other (str):
            country (str):
            active (bool):
            expiration_date (str):
            allowed_ip_list (list[str]):
            locale_id (int):
        """
        self.id = user_id
        self.username = username
        self.last_login_date = last_login_date
        self.role_ids = role_ids
        self.team_ids = team_ids
        self.authentication_provider_id = authentication_provider_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.cell_phone_number = cell_phone_number
        self.job_title = job_title
        self.other = other
        self.country = country
        self.active = active
        self.expiration_date = expiration_date
        self.allowed_ip_list = allowed_ip_list
        self.locale_id = locale_id

    def __str__(self):
        return """User(id={}, username={}, last_login_date={}, role_ids={}, team_ids={}, 
        authentication_provider_id={}, first_name={}, last_name={}, email={}, phone_number={}, cell_phone_number={}, 
        job_title={}, other={}, country={}, active={}, expiration_date={}, allowed_ip_list={}, locale_id={})""".format(
            self.id, self.username, self.last_login_date, self.role_ids, self.team_ids, self.authentication_provider_id,
            self.first_name, self.last_name, self.email, self.phone_number, self.cell_phone_number, self.job_title,
            self.other, self.country, self.active, self.expiration_date, self.allowed_ip_list, self.locale_id
        )
