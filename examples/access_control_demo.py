
"""
Process CSV file like the following content:

FirstName,LastName,Username,Email,JobTitle,Phone,MobilePhone,Country,Other,LocaleCode,Password,ExpirationDate,ActiveUser,Teams,Roles
John,Smith,john,john.smith@sleep.net,,,333 666 111,,,,test,5/22/2023,TRUE,/CxServer/SP/Company/Users;/CxServer/SP/Checkmarx,Admin; SAST Admin
Bob,Han,bob,bob.han@dd.com,,,,,,,test,1/23/2021,FALSE,/CxServer;/CxServer/SP,SAST Reviewer; SAST Scanner

Locale ID, Code, and Display Name:
1, 'en-US', 'English (United States)',
2, 'fr-FR', 'French (France), français (France)',
3, 'ja-JP', 'Japanese (Japan), 日本語 (日本)',
4, 'ko-KR', 'Korean (Korea), 한국어(대한민국)',
5, 'pt-BR', 'Portuguese (Brazil), português (Brasil)',
6, 'ru-RU', 'Russian (Russia), русский (Россия)',
7, 'zh-CN', 'Chinese (Simplified, China), 中文(中国)',
8, 'zh-TW', 'Chinese (Traditional, Taiwan), 中文(台灣)',
9, 'es-ES', 'Spanish (Traditional, Spain), Español (tradicional, españa)'


Read CSV file content, check data format for each field, create users accordingly.

Report which line(number), which column has illegal data

process data line by line, record process progress (which line)

"""
import csv

from CheckmarxPythonSDK.CxRestAPISDK import AccessControlAPI


def get_users_from_csv_file(file_path):
    users = []
    with open(file_path, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            users.append(row)
    return users


def add_users_from_csv_file(users):
    """

    All locale:
    ['en-US', 'fr-FR', 'ja-JP', 'ko-KR', 'pt-BR', 'ru-RU', 'zh-CN', 'zh-TW', 'es-ES']

    Args:
        users:

    Returns:

    """
    ac = AccessControlAPI()
    all_users = ac.get_all_users()
    all_user_name = [user.username for user in all_users]
    all_user_email = [user.email for user in all_users]
    all_locale_code = [item.code for item in ac.get_all_system_locales()]
    all_roles = ac.get_all_roles()
    all_teams = ac.get_all_teams

    for index, user in enumerate(users):
        row_number = index + 2
        username = user.get("Username")
        if username in all_user_name:
            print("Row No.{}, Username: {} already taken, will ignore this line".format(row_number, username))
            continue

        email = user.get("Email")
        if email in all_user_email:
            print("Row No.{}, Email: {} already taken, will ignore this line".format(row_number, email))
            continue

        try:
            locale_id = all_locale_code.index(user.get("LocaleCode")) + 1
        except ValueError:
            print("Wrong Locale Code in row No.{}, will use en-US".format(row_number))
            locale_id = 1

        role_ids = []
        for role_name in user.get("Roles").split(";"):
            for item in all_roles:
                if item.name == role_name:
                    role_ids.append(item.id)

        team_ids = []
        for team_name in user.get("Teams").split(";"):
            for item in all_teams:
                if item.full_name == team_name:
                    team_ids.append(item.id)

        ac.create_new_user(
            username=user.get("Username"),
            password=user.get("Password"),
            role_ids=role_ids,
            team_ids=team_ids,
            authentication_provider_id=1,
            first_name=user.get("FirstName"),
            last_name=user.get("LastName"),
            email=user.get("Email"),
            phone_number=user.get("Phone"),
            cell_phone_number=user.get("MobilePhone"),
            job_title=user.get("JobTitle"),
            other=user.get("Other"),
            country=user.get("Country"),
            active=user.get("ActiveUser").lower(),
            expiration_date=user.get("ExpirationDate"),
            allowed_ip_list=[],
            locale_id=locale_id,
        )


if __name__ == "__main__":
    users = get_users_from_csv_file(r"C:\Users\HappyY\Documents\SourceCode\GitHub\checkmarx-python-sdk\examples\CxSAST_appliation_users.csv")
    add_users_from_csv_file(users=users)
