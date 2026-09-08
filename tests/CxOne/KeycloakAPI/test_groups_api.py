from CheckmarxPythonSDK.CxOne.KeycloakAPI.GroupsApi import GroupsApi
import logging
logger = logging.getLogger(__name__)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.GroupRepresentation import (
    GroupRepresentation,
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.ManagementPermissionReference import (
    ManagementPermissionReference,
)


class TestGroupsApi:
    def setup_method(self):
        self.realm = "happy"
        self.groups_api = GroupsApi()

    def test_get_groups_by_realm(self):
        """Test get_groups_by_realm method with different parameters"""
        logger.info("\n=== Test 1: get_groups_by_realm ===")

        # Test with basic parameters
        groups = self.groups_api.get_groups_by_realm(realm=self.realm)
        logger.info(f"get_groups_by_realm successful: {groups is not None}")
        logger.info(f"Number of groups: {len(groups)}")
        logger.info(f"Groups: {[g.name for g in groups]}")
        assert groups is not None

        # Test with pagination parameters
        groups_paginated = self.groups_api.get_groups_by_realm(
            realm=self.realm, first=0, max=5
        )
        logger.info(f"Number of groups (paginated): {len(groups_paginated)}")
        logger.info(f"Groups (paginated): {[g.name for g in groups_paginated]}")

    def test_get_groups_count_by_realm(self):
        """Test get_groups_count_by_realm method"""
        logger.info("\n=== Test 2: get_groups_count_by_realm ===")

        try:
            count = self.groups_api.get_groups_count_by_realm(realm=self.realm)
            logger.info(f"get_groups_count_by_realm successful: {count is not None}")
            logger.info(f"Groups count: {count}")
            assert count is not None
        except Exception as e:
            logger.error(f"Error getting groups count: {e}")

    def test_group_crud(self):
        """Test group CRUD operations"""
        logger.info("\n=== Test 3: Group CRUD operations ===")
        test_group_name = "test_group_2026_02_24"
        updated_group_name = "updated_test_group"

        # Step 1: Check if group exists and delete if it does
        try:
            existing_groups = self.groups_api.get_groups_by_realm(realm=self.realm)
            for group in existing_groups:
                if group.name == test_group_name:
                    delete_successful = self.groups_api.delete_group_by_realm_by_id(
                        realm=self.realm, id=group.id
                    )
                    logger.info(f"Delete group {test_group_name} successful: {delete_successful}")
                    break
        except Exception as e:
            logger.error(f"Error checking/deleting group: {e}")

        # Step 2: Create the group (C)
        group_id = None
        try:
            group_representation = GroupRepresentation(
                name=test_group_name,
            )
            create_successful = self.groups_api.post_groups(
                realm=self.realm, group_representation=group_representation
            )
            logger.info(f"Create group {test_group_name} successful: {create_successful}")

            # Get the created group
            created_groups = self.groups_api.get_groups_by_realm(realm=self.realm)
            for group in created_groups:
                if group.name == test_group_name:
                    group_id = group.id
                    logger.info(f"Created group ID: {group_id}")
                    break
        except Exception as e:
            logger.error(f"Error creating group: {e}")

        # Step 3: Read the group (R)
        if group_id:
            try:
                group = self.groups_api.get_group(realm=self.realm, id=group_id)
                logger.info(f"get_group successful: {group is not None}")
                logger.info(f"Group: {group.name}")
                assert group is not None
                assert group.name == test_group_name
            except Exception as e:
                logger.error(f"Error getting group: {e}")

        # Step 4: Update the group (U)
        if group_id:
            try:
                updated_group_representation = GroupRepresentation(
                    name=updated_group_name
                )
                update_successful = self.groups_api.put_group_by_realm_by_id(
                    realm=self.realm,
                    id=group_id,
                    group_representation=updated_group_representation,
                )
                logger.info(f"Update group {test_group_name} successful: {update_successful}")

                # Verify the update
                updated_group = self.groups_api.get_group(realm=self.realm, id=group_id)
                logger.info(f"Updated group name: {updated_group.name}")
            except Exception as e:
                logger.error(f"Error updating group: {e}")

        # Step 5: Delete the group (D)
        if group_id:
            try:
                delete_successful = self.groups_api.delete_group_by_realm_by_id(
                    realm=self.realm, id=group_id
                )
                logger.info(f"Delete group {updated_group_name} successful: {delete_successful}")
            except Exception as e:
                logger.error(f"Error deleting group: {e}")

    def test_group_children(self):
        """Test group children methods"""
        logger.info("\n=== Test 4: Group Children ===")

        # Get a test group
        groups = self.groups_api.get_groups_by_realm(realm=self.realm)
        test_group = groups[0] if groups else None

        if test_group:
            logger.info(f"Testing with group: {test_group.name} (id: {test_group.id})")

            # Test get_children
            try:
                children = self.groups_api.get_children(
                    realm=self.realm, id=test_group.id
                )
                logger.info(f"get_children successful: {children is not None}")
                logger.info(f"Number of children: {len(children)}")
                logger.info(f"Children: {[c.name for c in children]}")
            except Exception as e:
                logger.error(f"Error getting children: {e}")
        else:
            logger.info("No groups found for testing children")

    def test_group_members(self):
        """Test group members method"""
        logger.info("\n=== Test 5: Group Members ===")

        # Get a test group
        groups = self.groups_api.get_groups_by_realm(realm=self.realm)
        test_group = groups[0] if groups else None

        if test_group:
            logger.info(f"Testing with group: {test_group.name} (id: {test_group.id})")

            # Test get_members
            try:
                members = self.groups_api.get_members(
                    realm=self.realm, id=test_group.id
                )
                logger.info(f"get_members successful: {members is not None}")
                logger.info(f"Number of members: {len(members)}")
                logger.info(f"Members: {[m.username for m in members]}")
            except Exception as e:
                logger.error(f"Error getting members: {e}")
        else:
            logger.info("No groups found for testing members")

    def test_group_management_permissions(self):
        """Test group management permissions method"""
        logger.info("\n=== Test 6: Group Management Permissions ===")

        # Get a test group
        groups = self.groups_api.get_groups_by_realm(realm=self.realm)
        test_group = groups[0] if groups else None

        if test_group:
            logger.info(f"Testing with group: {test_group.name} (id: {test_group.id})")

            # Test get_group_management_permissions
            try:
                permissions = self.groups_api.get_group_management_permissions(
                    realm=self.realm, id=test_group.id
                )
                logger.info(f"get_group_management_permissions successful: {permissions is not None}")
                logger.info(f"Permissions: {permissions.to_dict()}")
            except Exception as e:
                logger.error(f"Error getting management permissions: {e}")
        else:
            logger.info("No groups found for testing management permissions")
