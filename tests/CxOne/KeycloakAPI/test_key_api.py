from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    KeyApi,
)

realm = "happy"
key_api = KeyApi()

def test_get_keys():
    """Test get_keys method"""
    print("\n=== Test 1: get_keys ===")
    
    try:
        keys_metadata = key_api.get_keys(realm=realm)
        print(f"get_keys successful: {keys_metadata is not None}")
        print(f"Keys metadata: {keys_metadata.to_dict()}")
        assert keys_metadata is not None
        assert keys_metadata.keys is not None
        print(f"Number of keys: {len(keys_metadata.keys)}")
        for key in keys_metadata.keys:
            print(f"  - Key: {key.kid}, Type: {key.type}, Algorithm: {key.algorithm}, Use: {key.use}")
    except Exception as e:
        print(f"Error getting keys: {e}")
        raise

if __name__ == "__main__":
    test_get_keys()
    print("\n=== All KeyApi methods tested successfully! ===")
