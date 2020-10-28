# encoding: utf-8


class MyProfile(object):

    def __init__(self, profile_id, username, first_name, last_name, email, phone_number, cellphone_number, job_title,
                 other, country, locale_id, teams, authentication_provider_id):
        """

        Args:
            profile_id (int):
            username (str):
            first_name (str):
            last_name (str):
            email (str):
            phone_number (str):
            cellphone_number (str):
            job_title (str):
            other (str):
            country (str):
            locale_id (int):
            teams (str):
            authentication_provider_id (int):
        """
        self.id = profile_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.cellphone_number = cellphone_number
        self.job_title = job_title
        self.other = other
        self.country = country
        self.locale_id = locale_id
        self.teams = teams
        self.authentication_provider_id = authentication_provider_id

    def __str__(self):
        return """MyProfile(id={}, username={}, first_name={}, last_name={}, email={}, phone_number={}, 
        cellphone_number={}, job_title={}, other={}, country={}, locale_id={}, teams={}, 
        authentication_provider_id={})""".format(
            self.id, self.username, self.first_name, self.last_name, self.email, self.phone_number,
            self.cellphone_number, self.job_title, self.other, self.country, self.locale_id, self.teams,
            self.authentication_provider_id
        )
