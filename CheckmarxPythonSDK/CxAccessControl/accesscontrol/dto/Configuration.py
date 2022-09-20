class Configuration(object):
    def __init__(self, registration_link, is_assign_all_roles_by_manage_users_enabled, is_multitenancy_mode):
        self.registration_link = registration_link
        self.is_assign_all_roles_by_manage_users_enabled = is_assign_all_roles_by_manage_users_enabled
        self.is_multitenancy_mode = is_multitenancy_mode

    def __str__(self):
        return """Configuration(registration_link={}, 
        is_assign_all_roles_by_manage_users_enabled={}, is_multitenancy_mode={})""".format(
            self.registration_link, self.is_assign_all_roles_by_manage_users_enabled, self.is_multitenancy_mode
        )
