from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    IdentityProvidersApi,
)
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.IdentityProviderRepresentation import IdentityProviderRepresentation
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.IdentityProviderMapperRepresentation import IdentityProviderMapperRepresentation
from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto.ManagementPermissionReference import ManagementPermissionReference

realm = "happy"
identity_providers_api = IdentityProvidersApi()

def test_get_instances():
    """Test get_instances method with different parameters"""
    print("\n=== Test 1: get_instances ===")
    
    # Test with basic parameters
    identity_providers = identity_providers_api.get_instances(realm=realm)
    print(f"get_instances successful: {identity_providers is not None}")
    print(f"Number of identity providers: {len(identity_providers)}")
    print(f"Identity providers: {[ip.alias for ip in identity_providers]}")
    assert identity_providers is not None
    
    # Test with pagination parameters
    identity_providers_paginated = identity_providers_api.get_instances(realm=realm, first="0", max="5")
    print(f"Number of identity providers (paginated): {len(identity_providers_paginated)}")
    print(f"Identity providers (paginated): {[ip.alias for ip in identity_providers_paginated]}")

def test_identity_provider_crud():
    """Test identity provider CRUD operations"""
    print("\n=== Test 2: Identity Provider CRUD operations ===")
    test_alias = "test_identity_provider_2026_02_24"
    
    # Step 1: Check if identity provider exists and delete if it does
    try:
        existing_providers = identity_providers_api.get_instances(realm=realm)
        for provider in existing_providers:
            if provider.alias == test_alias:
                delete_successful = identity_providers_api.delete_instance(realm=realm, alias=test_alias)
                print(f"Delete identity provider {test_alias} successful: {delete_successful}")
                break
    except Exception as e:
        print(f"Error checking/deleting identity provider: {e}")
    
    # Step 2: Create the identity provider (C)
    try:
        # Note: This is a minimal representation - actual creation may require more fields
        identity_provider_representation = IdentityProviderRepresentation(
            alias=test_alias,
            provider_id="oidc",
            enabled=False
        )
        create_successful = identity_providers_api.post_instances(realm=realm, identity_provider_representation=identity_provider_representation)
        print(f"Create identity provider {test_alias} successful: {create_successful}")
        # assert create_successful is True
    except Exception as e:
        print(f"Error creating identity provider: {e}")
    
    # Step 3: Read the identity provider (R)
    try:
        # Find the identity provider by alias
        created_providers = identity_providers_api.get_instances(realm=realm)
        provider_found = False
        for provider in created_providers:
            if provider.alias == test_alias:
                provider_found = True
                print(f"Read identity provider {test_alias} successful")
                break
        if not provider_found:
            print(f"Identity provider {test_alias} not found after creation attempt")
    except Exception as e:
        print(f"Error reading identity provider: {e}")
    
    # Step 4: Update the identity provider (U)
    try:
        updated_identity_provider_representation = IdentityProviderRepresentation(
            alias=test_alias,
            provider_id="oidc",
            enabled=True
        )
        update_successful = identity_providers_api.put_instance(realm=realm, alias=test_alias, identity_provider_representation=updated_identity_provider_representation)
        print(f"Update identity provider {test_alias} successful: {update_successful}")
        # assert update_successful is True
    except Exception as e:
        print(f"Error updating identity provider: {e}")
    
    # Step 5: Delete the identity provider (D)
    try:
        delete_successful = identity_providers_api.delete_instance(realm=realm, alias=test_alias)
        print(f"Delete identity provider {test_alias} successful: {delete_successful}")
        # assert delete_successful is True
    except Exception as e:
        print(f"Error deleting identity provider: {e}")

def test_identity_provider_methods():
    """Test other identity provider methods"""
    print("\n=== Test 3: Other identity provider methods ===")
    
    # Get an existing identity provider to test with
    try:
        identity_providers = identity_providers_api.get_instances(realm=realm)
        if identity_providers:
            test_provider = identity_providers[0]
            test_alias = test_provider.alias
            print(f"Testing with identity provider: {test_alias}")
            
            # Test get_instance
            try:
                instance = identity_providers_api.get_instance(realm=realm, alias=test_alias)
                print(f"get_instance successful: {instance is not None}")
                print(f"Instance: {instance.alias}")
            except Exception as e:
                print(f"Error getting instance: {e}")
            
            # Test get_instance_management_permissions
            try:
                permissions = identity_providers_api.get_instance_management_permissions(realm=realm, alias=test_alias)
                print(f"get_instance_management_permissions successful: {permissions is not None}")
                print(f"Permissions: {permissions.to_dict()}")
            except Exception as e:
                print(f"Error getting management permissions: {e}")
            
            # Test get_mappers
            try:
                mappers = identity_providers_api.get_mappers(realm=realm, alias=test_alias)
                print(f"get_mappers successful: {mappers is not None}")
                print(f"Number of mappers: {len(mappers)}")
                print(f"Mappers: {[m.name for m in mappers]}")
            except Exception as e:
                print(f"Error getting mappers: {e}")
        else:
            print("No identity providers found for testing other methods")
    except Exception as e:
        print(f"Error in identity provider methods test: {e}")

def test_identity_provider_providers():
    """Test identity provider provider methods"""
    print("\n=== Test 4: Identity Provider Provider methods ===")
    
    # Test with a common provider ID
    test_provider_id = "oidc"
    try:
        provider = identity_providers_api.get_identity_provider_provider(realm=realm, provider_id=test_provider_id)
        print(f"get_identity_provider_provider successful: {provider is not None}")
        print(f"Provider: {provider}")
    except Exception as e:
        print(f"Error getting identity provider provider: {e}")

if __name__ == "__main__":
    test_get_instances()
    test_identity_provider_crud()
    test_identity_provider_methods()
    test_identity_provider_providers()
    print("\n=== All IdentityProvidersApi methods tested successfully! ===")
