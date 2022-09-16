from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI, config


class ConfigOverride:

    keys = ['base_url', 'username', 'password']

    def __init__(self, new_config):

        self.new_config = new_config
        self.old_config = {}

    def __enter__(self):

        for key in self.keys:
            self.old_config[key] = config.config[key]
            config.config[key] = self.new_config[key]

    def __exit__(self, exc_type, exc_value, traceback):

        for key in self.keys:
            config.config[key] = self.old_config[key]


configs = {
    'dst': {
        'base_url': ' http://HappyY-Laptop',
        'username': 'Admin',
        'password': 'Password01!'
    },
    'src': {
        'base_url': ' http://192.168.3.84',
        'username': 'Admin',
        'password': 'Password01!'
    }
}

teamAPI = TeamAPI()
for c in configs.values():
    print(f'Retrieving data from {c["base_url"]}')
    with ConfigOverride(c):
        teams = teamAPI.get_all_teams()
        print(f'Found {len(teams)} teams')
        if len(teams) == 0:
            print('Trying again...')
            teams = teamAPI.get_all_teams
            print(f'Found {len(teams)} teams')
