
"""
Process CSV file like the following content:

Number,First Name(required),Last Name(required),Username(required),Email(required),Job Title,Phone,Mobile Phone,Country,Other,Locale,Password(required),Expiration Date,Active User(required),Teams(required),Roles
1,John,Smith,john,john.smith@sleep.net,,,333 666 111,,,,test,5/22/2023,TRUE,/CxServer/SP/Company/Users;/CxServer/SP/Checkmarx,Admin; SAST Admin
2,Bob,Han,bob,bob.han@dd.com,,,,,,,test,1/23/2021,FALSE,/CxServer;/CxServer/SP,SAST Reviewer; SAST Scanner

Read CSV file content, check data format for each field, create users accordingly.

Report which line(number), which column has illegal data

process data line by line, record process progress (which line)

"""

from CheckmarxPythonSDK.CxRestAPISDK import AccessControlAPI


def add_users_from_csv_file():
    ac = AccessControlAPI()
    # TODO


if __name__ == "__main__":
    add_users_from_csv_file()
