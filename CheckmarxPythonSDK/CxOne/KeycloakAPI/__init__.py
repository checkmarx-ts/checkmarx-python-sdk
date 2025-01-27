from .ClientsAPI import (
    get_all_oauth_clients,
    get_oauth_client_by_name,
    get_all_oauth_client_by_id,
    create_oauth_client,
    edit_auth_client,
    get_oauth_service_account_user,
    add_group_to_oauth_client,
    generate_oauth_secret,
    get_client_ast_app,
)
from .RootAPI import get_realms

from .UsersAPI import (
    get_users,
    get_user_id_by_name,
    get_user_id_list_by_username_list,
    get_user_id_by_email,
    get_user_id_list_by_email_list,
    create_a_new_user,
    get_number_of_users_by_given_criteria,
    delete_user,
    get_users_profile,
    get_users_profile_metadata,
    get_user_by_id,
    update_user_by_id,
)

from .GroupsAPI import (
    get_group_hierarchy,
    create_group_set,
    get_group_by_name,
    get_number_of_groups_in_a_realm,
    get_group_by_id,
    update_group_by_id,
    delete_group_by_id,
    create_subgroup,
    get_group_permissions,
    update_group_permissions,
    get_group_members,
    create_group,
)

from .RoleMapperAPI import (
    get_role_mappings,
)


from .RolesAPI import (
    get_all_roles_for_the_client,
    create_role_for_the_client,
    delete_role_by_name,
    get_role_by_name,
    update_role_by_id,
    get_roles_children,
    get_roles_children_iam,
    add_children_to_a_composite_role,
    get_all_roles_for_the_realm,
)
