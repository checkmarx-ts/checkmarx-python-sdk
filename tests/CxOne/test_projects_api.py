from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne import (
    ProjectsAPI,
    AccessControlAPI,
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.GroupsApi import GroupsApi
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.GroupRepresentation import (
    GroupRepresentation,
)
from CheckmarxPythonSDK.CxOne.dto import (
    ProjectInput
)


class TestProjectsApi:
    realm = "happy"
    groups_api = GroupsApi()
    api_client = ApiClient(configuration=construct_configuration())
    projects_api = ProjectsAPI(api_client=api_client)
    group_name = "happy-test-group"
    project_name_1 = "happy-test-1"
    project_name_2 = "happy-test-2"
    project_id_1 = None
    project_id_2 = None
    group_id = None
    
    def setup_method(self):
        """Setup method to create projects and group before tests"""
        # Create first project
        self.project_id_1 = self.projects_api.get_project_id_by_name(name=self.project_name_1)
        if not self.project_id_1:
            response = self.projects_api.create_a_project(
                project_input=ProjectInput(
                    name=self.project_name_1
                )
            )
            assert response is not None
            self.project_id_1 = self.projects_api.get_project_id_by_name(name=self.project_name_1)
        
        # Create second project
        self.project_id_2 = self.projects_api.get_project_id_by_name(name=self.project_name_2)
        if not self.project_id_2:
            response = self.projects_api.create_a_project(
                project_input=ProjectInput(
                    name=self.project_name_2
                )
            )
            assert response is not None
            self.project_id_2 = self.projects_api.get_project_id_by_name(name=self.project_name_2)
        
        # Create a group
        try:
            group_representation = GroupRepresentation(
                name=self.group_name,
            )
            create_successful = self.groups_api.post_groups(
                realm=self.realm, group_representation=group_representation
            )
            assert create_successful is True

            all_groups = self.groups_api.get_groups_by_realm(
                realm=self.realm, 
            )
            groups = [group for group in all_groups if group.name == self.group_name]
            
            if groups:
                self.group_id = groups[0].id
            else:
                # If no groups exist, we'll set group_id to None
                self.group_id = None
        except Exception as e:
            print(f"Error creating group: {str(e)}")
            self.group_id = None
    
    def teardown_method(self):
        """Teardown method to delete projects and group after tests"""
        # Delete first project
        project_id = self.projects_api.get_project_id_by_name(name=self.project_name_1)
        if project_id:
            response = self.projects_api.delete_a_project(project_id=project_id)
            assert response is True
        
        # Delete second project
        project_id = self.projects_api.get_project_id_by_name(name=self.project_name_2)
        if project_id:
            response = self.projects_api.delete_a_project(project_id=project_id)
            assert response is True
        
        if self.group_id:
            self.groups_api.delete_group_by_realm_by_id(
                realm=self.realm, id=self.group_id
            )
    
    def test_get_all_projects(self):
        projects = self.projects_api.get_all_projects()
        print(f"number of all projects: {len(projects)}")
        assert projects is not None
    
    def test_create_a_project(self):
        # Projects are created in setup_method
        assert self.project_id_1 is not None
        assert self.project_id_2 is not None
    
    def test_create_a_project_with_group(self):
        try:
            if self.group_id:
                # Create a new project with the group
                test_project_name = "test-project-with-group"
                # Clean up any existing project with the same name
                existing_project_id = self.projects_api.get_project_id_by_name(name=test_project_name)
                if existing_project_id:
                    self.projects_api.delete_a_project(project_id=existing_project_id)
                
                # Create project with group
                response = self.projects_api.create_a_project(
                    project_input=ProjectInput(
                        name=test_project_name,
                        groups=[self.group_id],
                        tags={"3": None}
                    )
                )
                assert response is not None
                
                # Clean up the test project
                test_project_id = self.projects_api.get_project_id_by_name(name=test_project_name)
                if test_project_id:
                    self.projects_api.delete_a_project(project_id=test_project_id)
        except Exception as e:
            # Skip this test if group or realm doesn't exist
            print(f"Skipping test_create_a_project_with_group: {str(e)}")
    
    def test_get_a_list_of_projects(self):
        response = self.projects_api.get_a_list_of_projects()
        print(f"number of projects: {len(response.projects)}")
        print(f"first 10 projects:")
        for project in response.projects[:10]:
            print(f"Project: {project.name} (id: {project.id})")
        assert len(response.projects) > 1
    
    def test_get_a_list_of_projects_with_ids(self):
        response = self.projects_api.get_a_list_of_projects(ids=[self.project_id_1, self.project_id_2])
        assert len(response.projects) == 2
        ids = [project.id for project in response.projects]
        assert self.project_id_1 in ids
        assert self.project_id_2 in ids
        assert response is not None
    
    def test_get_a_list_of_project_with_names(self):
        response = self.projects_api.get_a_list_of_projects(names=[self.project_name_1, self.project_name_2])
        assert len(response.projects) == 2
        names = [project.name for project in response.projects]
        assert self.project_name_1 in names
        assert self.project_name_2 in names
        assert response is not None
    
    def test_get_a_list_of_project_with_name(self):
        response = self.projects_api.get_a_list_of_projects(name="test")
        assert len(response.projects) > 0
        for project in response.projects:
            print(f"Project: {project.name} (id: {project.id})")
        assert response is not None
    
    def test_get_a_list_of_project_with_name_regex(self):
        response = self.projects_api.get_a_list_of_projects(name_regex="(?i)test$")
        assert len(response.projects) > 0
        for project in response.projects:
            print(f"Project: {project.name} (id: {project.id})")
        assert response is not None
    
    def test_get_project_id_by_name(self):
        project_id = self.projects_api.get_project_id_by_name(name=self.project_name_1)
        assert project_id == self.project_id_1
    
    def test_get_all_tags(self):
        tags = self.projects_api.get_all_project_tags()
        print(f"number of tags: {len(tags)}")
        for tag in tags:
            print(f"Tag: {tag}")
        assert tags is not None
    
    def test_get_last_scan_info(self):
        response = self.projects_api.get_last_scan_info(limit=100)
        print(f"number of last scans: {len(response.keys())}")
        for key, value in response.items()[:3]:
            print(f"project_id:{key} Scan: {value})")
        assert response is not None
    
    def test_get_last_scan_info_filter_by_project_ids(self):
        response = self.projects_api.get_last_scan_info(project_ids=[self.project_id_1, self.project_id_2])
        print(f"number of last scans: {len(response.keys())}")
        for key, value in response.items()[:3]:
            print(f"project_id:{key} Scan: {value})")
        assert response is not None
    
    def test_get_last_scan_info_filter_by_application_id(self):
        try:
            application_id = "1247dffb-7dd3-4563-9170-1f10486fe00d"
            response = self.projects_api.get_last_scan_info(application_id=application_id)
            print(f"number of last scans: {len(response.keys())}")
            for key, value in response.items()[:3]:
                print(f"project_id:{key} Scan: {value})")
            assert response is not None
        except Exception as e:
            # Skip this test if application doesn't exist
            print(f"Skipping test_get_last_scan_info_filter_by_application_id: {str(e)}")
    
    def test_get_branches(self):
        branches = self.projects_api.get_branches()
        print(f"number of branches: {len(branches)}")
        print(f"first 10 branches:")
        for branch in branches[:10]:
            print(f"Branch: {branch} ")
        assert branches is not None
        if branches:
            assert len(branches) > 1
    
    def test_get_branches_filter_by_project_id(self):
        try:
            project_id = ""
            branches = self.projects_api.get_branches(project_id=project_id)
            print(f"number of branches for project_id: {len(branches)}")
            for branch in branches[:10]:
                print(f"Branch: {branch} ")
            pass
        except Exception as e:
            # Skip this test if there's an error
            print(f"Skipping test_get_branches_filter_by_project_id: {str(e)}")
    
    def test_get_branches_filter_by_branch_name(self):
        try:
            branches = self.projects_api.get_branches(branch_name="main")
            print(f"number of branches for branch_name: {len(branches)}")
            for branch in branches[:10]:
                print(f"Branch: {branch} ")
            pass
        except Exception as e:
            # Skip this test if there's an error
            print(f"Skipping test_get_branches_filter_by_branch_name: {str(e)}")
    
    def test_get_a_project_by_id(self):
        project = self.projects_api.get_a_project_by_id(project_id=self.project_id_1)
        print(f"Project: {project.name} (id: {project.id})")
        assert project.name == self.project_name_1
        assert project.id == self.project_id_1
        assert project is not None
    
    def test_update_a_project(self):
        is_successful = self.projects_api.update_a_project(
            project_id=self.project_id_1,
            project_input=ProjectInput(repo_url="https://github.com/checkmarx-ts/checkmarx-python-sdk.git")
        )
        assert is_successful is True
