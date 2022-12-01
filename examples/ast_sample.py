from CheckmarxPythonSDK.CxOne import (

    get_a_list_of_applications,

    get_application_id_by_name,

)

from CheckmarxPythonSDK.CxOne import (

    get_a_list_of_projects,

    get_project_id_by_name,

    get_last_scan_info,

    get_a_project_by_id,

)



if __name__ == '__main__':

    # Get a list of all applications

    ast_applications = get_a_list_of_applications()

    print(ast_applications)
